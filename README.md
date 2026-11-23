# trace — independent on-chain verification

**[فارسی](#فارسی) · [English](#english)**

---

## English

This repository lets anyone re-check, **directly against public blockchain nodes**, every on-chain figure published at **[trace.avoxova.com](https://trace.avoxova.com)**.

That site follows a 100 USDT (BEP-20) payment made in November 2026 (Aban 1405) on the domain **dotomarket1.com**, which presented itself as a sale of the DOTO token. The tracing was done independently by the AVOXOVA AI agent.

> This case concerns **only the domain dotomarket1.com**. It makes no claim about the DOTO token itself, its issuer, or any other website. Listing an address here is a statement about public blockchain data, not an accusation against its holder. Exchanges, custodians and bridges appear only as *destinations* or *infrastructure*.

### Run it

Requirements: Python 3.9+ and internet access. No packages and no API keys are needed.

```bash
git clone https://github.com/avoxova/trace.git
cd trace
python3 verify.py            # human-readable
python3 verify.py --json     # machine-readable
```

The exit code is `0` when nothing fails and `1` when any claim fails.

### What it checks

All claims are listed in [`claims.json`](claims.json). Each one is checked live:

| Chain | What is verified |
|---|---|
| BNB Smart Chain | The 100 USDT deposit, and the sweep 2 minutes later (95 USDT to the collection wallet and 5 USDT to a referrer). Every hop of paths A, B and C toward the NEAR Intents bridge, plus the unlimited approval of path C. The sale contract's `owner()` and `treasury()`. The collection wallet's current balance. |
| XRP Ledger | The three USDT→XRP conversion payouts. Every intermediate hop. All 8 deposits into Cobo Custody across 4 destination tags, with per-tag totals of about 175,000 XRP. The payments into the MEXC-linked wallet and that wallet's activation by MEXC's labelled account. The holding wallet. |
| XRPScan | The public labels "Cobo Custody" and "MEXC". |

### Known limits — please help

- **Archive-only:** the collection wallet's balance right before and after the sweep (101,965.98 → 102,060.98 USDT) needs an archive BSC node. Free public nodes only keep recent state. If you have one, run:
  `python3 verify.py --bsc-rpc https://your-archive-node`
- **Not yet scripted:** the site's aggregate statistics (number of senders and deposits into the collection wallet) need full log indexing. Free public RPCs rate-limit this. A PR that adds a robust and reproducible counter is very welcome.
- **Path C is marked *probable*:** its link to the bridge payout is inferred from an unlimited approval, not from a direct transfer.
- **Timestamps** are printed in UTC. The site shows Tehran time (UTC+3:30).

### Contributing

Open an issue or a pull request if any of these applies:
- a check fails,
- a figure is wrong,
- you can verify the archive-only items,
- you can improve methodology.

Please keep contributions to verifiable on-chain facts. Do not post personal data or accusations.

**Not legal advice.** This is a technical record of public data. Victims should file a complaint with the judicial authority and the cyber police ([policefata.ir](https://policefata.ir)).

---

## فارسی

این مخزن به هر کسی امکان می‌دهد تمام داده‌های بلاکچینی منتشرشده در **[trace.avoxova.com](https://trace.avoxova.com)** را **مستقیم از نودهای عمومی بلاکچین** دوباره بررسی کند.

موضوع آن سایت ردیابی یک پرداخت ۱۰۰ تتری (BEP-20) است. این پرداخت در آبان ۱۴۰۵ در دامنه‌ی **dotomarket1.com** انجام شد؛ دامنه‌ای که با عنوان فروش ارز DOTO فعالیت می‌کرد. ردیابی به‌صورت مستقل توسط ایجنت هوش مصنوعی AVOXOVA انجام شده است.

> این پرونده **فقط به دامنه‌ی dotomarket1.com** مربوط است و درباره‌ی خود توکن DOTO، صادرکننده‌ی آن یا هیچ سایت دیگری ادعایی ندارد. آمدن یک آدرس در این مخزن، بیان داده‌ی عمومی بلاکچین است و اتهامی به دارنده‌ی آن نیست. صرافی‌ها، امانت‌دارها و پل‌ها فقط به‌عنوان *مقصد* یا *زیرساخت* ذکر شده‌اند.

### اجرا

فقط پایتون ۳.۹ به بالا و اینترنت لازم است. نصب بسته یا کلید API لازم نیست.

```bash
git clone https://github.com/avoxova/trace.git
cd trace
python3 verify.py
```

برای هر ادعا یکی از این نتایج نمایش داده می‌شود:
- `PASS`: تأیید شد
- `FAIL`: رد شد
- `SKIP`: نیاز به نود آرشیوی دارد

### چه چیزهایی بررسی می‌شود

**در شبکه‌ی BSC:**
- واریز ۱۰۰ تتر، و جاروی آن دو دقیقه بعد (۹۵ تتر به کیف جمع‌آوری و ۵ تتر به معرف)
- همه‌ی گام‌های مسیرهای الف، ب و ج تا پل NEAR Intents
- مالک و خزانه‌ی قرارداد فروش

**در شبکه‌ی ریپل:**
- سه تبدیل تتر به ریپل و همه‌ی گام‌های میانی
- هشت واریز به Cobo (امانت‌دار دارایی) با چهار تگ و مجموع حدود ۱۷۵ هزار XRP
- واریزها به کیف مرتبط با MEXC

### محدودیت‌ها

- **نیاز به نود آرشیوی:** موجودی کیف جمع‌آوری دقیقاً پیش و پس از جارو، از نودهای رایگان قابل‌بررسی نیست.
- **هنوز اسکریپت نشده:** آمار کلی (تعداد فرستنده‌ها و واریزها) به ایندکس کامل لاگ‌ها نیاز دارد. نودهای رایگان این کار را محدود می‌کنند و از کمک توسعه‌دهندگان استقبال می‌کنیم.
- **مسیر ج «احتمالی» است:** پیوند آن با پل از یک مجوز برداشت (approve) استنباط شده، نه از انتقال مستقیم.

### مشارکت

اگر خطایی دیدید یا روش بهتری دارید، issue یا pull request بفرستید. لطفاً فقط داده‌ی قابل‌بازبینی بلاکچین بفرستید و داده‌ی شخصی یا اتهام نفرستید.

**این مخزن مشاوره‌ی حقوقی نیست.** مال‌باختگان ابتدا به مرجع قضایی و سپس به پلیس فتا ([policefata.ir](https://policefata.ir)) مراجعه کنند.

---

[avoxova.com](https://avoxova.com) · [agent.avoxova.com](https://agent.avoxova.com) · [Telegram](https://t.me/avoxova) · [Instagram](https://www.instagram.com/avoxova/)
