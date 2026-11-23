#!/usr/bin/env python3
"""
trace-verify: independently re-check every on-chain claim of
https://trace.avoxova.com against public BNB Smart Chain and XRP Ledger nodes.

Standard library only. Usage:
    python3 verify.py                 # check everything
    python3 verify.py --json          # machine-readable output
    python3 verify.py --bsc-rpc URL   # use your own (archive) BSC node
    python3 verify.py --xrpl-rpc URL  # use your own XRPL node
"""
import argparse
import json
import os
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {"Content-Type": "application/json", "User-Agent": "trace-verify/1.0 (+https://github.com/avoxova/trace)"}
BSC_RPCS = ["https://bsc-rpc.publicnode.com", "https://bsc-dataseed.binance.org", "https://bsc.drpc.org"]
XRPL_RPCS = ["https://xrplcluster.com", "https://s1.ripple.com:51234", "https://xrpl.ws"]
XRPSCAN = "https://api.xrpscan.com/api/v1/account/"
TRANSFER = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
APPROVAL = "0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925"
SEL = {"owner": "0x8da5cb5b", "treasury": "0x61d027b3", "balanceOf": "0x70a08231"}
RIPPLE_EPOCH = 946684800


def post(url, body, timeout=40):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def get(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA["User-Agent"]})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


class Chain:
    def __init__(self, bsc, xrpl):
        self.bsc, self.xrpl = bsc, xrpl

    def eth(self, method, params):
        last = None
        for u in self.bsc:
            for _ in range(2):
                try:
                    r = post(u, {"jsonrpc": "2.0", "id": 1, "method": method, "params": params})
                    if "error" in r:
                        last = r["error"]
                        break
                    return r["result"]
                except Exception as e:  # network hiccup -> retry / next node
                    last = e
                    time.sleep(1)
        raise RuntimeError(f"{method}: {last}")

    def xrp(self, method, params):
        last = None
        for u in self.xrpl:
            for _ in range(2):
                try:
                    r = post(u, {"method": method, "params": [params]})["result"]
                    if r.get("status") == "error":
                        last = r.get("error")
                        break
                    return r
                except Exception as e:
                    last = e
                    time.sleep(1)
        raise RuntimeError(f"{method}: {last}")


def addr(topic):
    return "0x" + topic[-40:].lower()


def usdt(hexval):
    return int(hexval, 16) / 1e18


class Report:
    def __init__(self):
        self.rows = []

    def add(self, cid, title, status, detail=""):
        self.rows.append({"id": cid, "title": title, "status": status, "detail": detail})
        mark = {"PASS": "\u2714 PASS", "FAIL": "\u2718 FAIL", "SKIP": "- SKIP", "ERROR": "! ERROR"}[status]
        if not ARGS.json:
            print(f"{mark:8} [{cid}] {title}" + (f"  ({detail})" if detail else ""), flush=True)


def check(rep, cid, title, fn):
    try:
        ok, detail = fn()
        rep.add(cid, title, "PASS" if ok else "FAIL", detail)
    except Exception as e:
        rep.add(cid, title, "ERROR", str(e)[:160])


def run(c, chain, rep):
    U = c["tokens"]["usdt_bsc"].lower()

    # --- BSC: USDT transfers inside specific transactions
    for t in c["bsc_transfers"]:
        def f(t=t):
            rc = chain.eth("eth_getTransactionReceipt", [t["tx"]])
            if not rc or rc["status"] != "0x1":
                return False, "receipt missing or reverted"
            logs = [(addr(l["topics"][1]), addr(l["topics"][2]), usdt(l["data"]))
                    for l in rc["logs"] if l["address"].lower() == U and l["topics"][0] == TRANSFER]
            miss = [x for x in t["transfers"]
                    if not any(a == x[0].lower() and b == x[1].lower() and abs(v - x[2]) < 0.01 for a, b, v in logs)]
            if "block" in t and int(rc["blockNumber"], 16) != t["block"]:
                return False, f"block {int(rc['blockNumber'], 16)}"
            if "to" in t and rc["to"].lower() != t["to"].lower():
                return False, f"tx.to {rc['to']}"
            return not miss, ("block " + str(int(rc["blockNumber"], 16))) if not miss else f"missing {miss}"
        check(rep, t["id"], t["title"], f)

    # --- BSC: approvals
    for a in c["bsc_approvals"]:
        def f(a=a):
            rc = chain.eth("eth_getTransactionReceipt", [a["tx"]])
            for l in rc["logs"]:
                if l["address"].lower() == U and l["topics"][0] == APPROVAL and addr(l["topics"][1]) == a["owner"].lower() \
                        and addr(l["topics"][2]) == a["spender"].lower():
                    unlimited = int(l["data"], 16) >= 2 ** 255
                    return unlimited == a.get("unlimited", unlimited), "unlimited" if unlimited else f"{usdt(l['data'])}"
            return False, "approval log not found"
        check(rep, a["id"], a["title"], f)

    # --- BSC: sale contract state (live)
    sale = c["contracts"]["sale"]
    for k in ("owner", "treasury"):
        def f(k=k):
            v = addr(chain.eth("eth_call", [{"to": sale, "data": SEL[k]}, "latest"]))
            return v == c["sale_state"][k].lower(), v
        check(rep, f"sale.{k}", f"Sale contract {k}() == {c['sale_state'][k]}", f)

    def code_exists(a):
        return lambda: (len(chain.eth("eth_getCode", [a, "latest"])) > 2, "contract code present")
    check(rep, "sale.code", "Sale contract has code", code_exists(sale))
    check(rep, "token.code", "DOTO token contract has code", code_exists(c["contracts"]["token"]))

    for b in c["bsc_balances_now"]:
        def f(b=b):
            v = usdt(chain.eth("eth_call", [{"to": U, "data": SEL["balanceOf"] + "0" * 24 + b["address"][2:].lower()}, "latest"]))
            return v <= b["max_usdt"], f"{v:.4f} USDT"
        check(rep, b["id"], b["title"], f)

    # --- BSC: archive-only claims
    for a in c["archive_only"]:
        def f(a=a):
            data = SEL["balanceOf"] + "0" * 24 + a["address"][2:].lower()
            try:
                pre = usdt(chain.eth("eth_call", [{"to": U, "data": data}, hex(a["block"] - 1)]))
                post_ = usdt(chain.eth("eth_call", [{"to": U, "data": data}, hex(a["block"])]))
            except RuntimeError as e:
                raise RuntimeError("needs an archive BSC node (--bsc-rpc): " + str(e)[:80])
            return abs(pre - a["before"]) < 0.01 and abs(post_ - a["after"]) < 0.01, f"{pre:.2f} -> {post_:.2f}"
        try:
            ok, d = f()
            rep.add(a["id"], a["title"], "PASS" if ok else "FAIL", d)
        except Exception as e:
            rep.add(a["id"], a["title"], "SKIP", str(e)[:140])

    # --- XRPL payments
    def xpay(cid, title, p):
        def f():
            r = chain.xrp("tx", {"transaction": p["hash"]})
            if r.get("meta", {}).get("TransactionResult") != "tesSUCCESS":
                return False, "not tesSUCCESS"
            ok = r["Account"] == p["src"] and r.get("Destination") == p["dst"]
            amt = r["meta"].get("delivered_amount")
            got = int(amt) / 1e6 if isinstance(amt, str) else None
            if "xrp" in p:
                ok = ok and got is not None and abs(got - p["xrp"]) < 0.01
            if "tag" in p:
                ok = ok and r.get("DestinationTag") == p["tag"]
            when = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime(r["date"] + RIPPLE_EPOCH))
            return ok, f"{got} XRP, tag {r.get('DestinationTag')}, {when}"
        check(rep, cid, title, f)

    for p in c["xrp_payments"]:
        xpay(p["id"], p["title"], p)
    cobo = c["cobo"]
    totals = {}
    for i, d in enumerate(cobo["deposits"], 1):
        xpay(f"cobo-{i}", f"Deposit to Cobo tag {d['tag']}", dict(d, dst=cobo["account"]))
        totals[str(d["tag"])] = totals.get(str(d["tag"]), 0) + d["xrp"]
    for tag, want in cobo["tag_totals"].items():
        check(rep, f"tag-{tag}", f"Tag {tag} total ~{want:,} XRP",
              lambda tag=tag, want=want: (abs(totals.get(tag, 0) - want) < 1, f"{totals.get(tag, 0):,.2f}"))
    check(rep, "cobo-total", f"Cobo total ~{cobo['total_approx']:,} XRP",
          lambda: (abs(sum(totals.values()) - cobo["total_approx"]) < 1000, f"{sum(totals.values()):,.2f}"))

    for a, label in c["xrpscan_labels"].items():
        def lab(a=a, label=label):
            d = get(XRPSCAN + a)
            names = json.dumps([d.get("accountName"), d.get("account_name"), d.get("tag")], ensure_ascii=False)
            return label.split()[0].lower() in names.lower(), names[:100]
        check(rep, f"label-{a[:6]}", f"XRPScan label of {a} mentions '{label}'", lab)


def main():
    global ARGS
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--claims", default=os.path.join(HERE, "claims.json"))
    ap.add_argument("--bsc-rpc", action="append", help="BSC JSON-RPC URL (repeatable). Archive node enables archive-only checks.")
    ap.add_argument("--xrpl-rpc", action="append", help="XRPL JSON-RPC URL (repeatable)")
    ap.add_argument("--json", action="store_true")
    ARGS = ap.parse_args()
    claims = json.load(open(ARGS.claims, encoding="utf-8"))
    chain = Chain(ARGS.bsc_rpc or BSC_RPCS, ARGS.xrpl_rpc or XRPL_RPCS)
    rep = Report()
    run(claims, chain, rep)
    s = {k: sum(r["status"] == k for r in rep.rows) for k in ("PASS", "FAIL", "SKIP", "ERROR")}
    if ARGS.json:
        print(json.dumps({"summary": s, "results": rep.rows}, indent=2, ensure_ascii=False))
    else:
        print("\n" + "  ".join(f"{k}: {v}" for k, v in s.items()))
    sys.exit(1 if s["FAIL"] else 0)


ARGS = None
if __name__ == "__main__":
    main()
