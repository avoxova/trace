# trace — independent on-chain verification

<p align="center">
  <b>📄 Public report:</b> <a href="https://trace.avoxova.com">trace.avoxova.com</a> (فارسی) · <a href="https://trace.avoxova.com/en">trace.avoxova.com/en</a> (English)
</p>

**[فارسی](#فارسی) · [English](#english)**

---

## English

### What this is

**[trace.avoxova.com](https://trace.avoxova.com)** is a public report about a phishing case on the domain **dotomarket1.com**. In November 2026 (Aban 1405) that domain collected payments under the title of a DOTO token sale. The AVOXOVA AI agent independently traced the money from one 100 USDT (BEP-20) payment. The trail runs on BNB Smart Chain, through a cross-chain bridge, and on the XRP Ledger, and ends at the services where the funds arrived.

**This repository is the open, reproducible side of that report.** Every on-chain figure on the site is listed in [`claims.json`](claims.json), and [`verify.py`](verify.py) re-checks each one live against public blockchain nodes. You do not need to trust us; you can run it yourself.

> This case concerns **only the domain dotomarket1.com**. It makes no claim about the DOTO token itself, its issuer, or any other website. Listing an address here is a statement about public blockchain data, not an accusation against its holder. Exchanges, custodians and bridges appear only as *destinations* or *infrastructure*.

### Why it is open: a call to developers

We opened this repository for developers and on-chain analysts who want to:

1. **Audit:** run the checker and tell us if any figure is wrong.
2. **Complete the trail:** follow the funds further than we did. See the open tasks below.
3. **Improve the method:** make the checks more robust, add sources, and reduce the parts that rely on inference.

Corrections are welcome even when they go against our own conclusions. Anything confirmed here will also be corrected on the public report.

### Run it

Requirements: Python 3.9+ and internet access. No packages and no API keys are needed.

```bash
git clone https://github.com/avoxova/trace.git
cd trace
python3 verify.py            # human-readable
python3 verify.py --json     # machine-readable
python3 verify.py --bsc-rpc https://your-archive-node   # enables archive-only checks
```

The exit code is `0` when nothing fails and `1` when any claim fails. On free public nodes the current result is **48 PASS, 0 FAIL, 1 SKIP** (the skip is archive-only). Timestamps are printed in UTC; the site shows Tehran time (UTC+3:30).

### What it checks

| Chain | What is verified |
|---|---|
| BNB Smart Chain | The 100 USDT deposit, and the sweep 2 minutes later (95 USDT to the collection wallet and 5 USDT to a referrer). Every hop of paths A, B and C toward the NEAR Intents bridge, plus the unlimited approval of path C. The sale contract's `owner()` and `treasury()`. The collection wallet's current balance. |
| XRP Ledger | The three USDT→XRP conversion payouts and every intermediate hop. All deposits into Cobo Custody across 4 destination tags. The payments into the MEXC-linked wallet and that wallet's activation by MEXC's labelled account. The holding wallet and its later forward to Cobo. |
| XRPScan | The public labels "Cobo Custody" and "MEXC". |

### Open tasks: help complete the trail

| # | Task | Why it is open |
|---|---|---|
| 1 | Verify the collection wallet's balance just before and after the sweep (101,965.98 → 102,060.98 USDT). | Needs an archive BSC node. |
| 2 | Reproducibly count senders and deposits into the collection wallet `0xe3df…988a` during 26–30 Aban 1405. | Free RPCs and explorers rate-limit full log scans. |
| 3 | Map the rest of the collection wallet's outflows, beyond paths A, B and C. | The site traces only the funds linked to one payment. |
| 4 | Confirm or reject the **probable** path C, which links feeder `0x5b6a…53fd` to the third XRP payout. | It is currently inferred from an unlimited approval, not from a direct transfer. |
| 5 | Follow the MEXC-linked wallet and the aggregator `r3GY…upLf` further. | Not yet traced. |

### Contributing

- Open an **issue** for a wrong figure, a failing check, or a new lead. Include transaction hashes, so it can be verified.
- Open a **pull request** to add a claim to `claims.json` together with its check in `verify.py`. Every new claim must be verifiable from public chain data with this script.
- Please do **not** post personal data, guesses about identities, or accusations. Keep to on-chain facts.

### Contact

For questions, corrections or leads that do not fit in a public issue, contact us on Telegram: **[@avoxova_support](https://t.me/avoxova_support)**. Updates are announced on the channel **[@avoxova](https://t.me/avoxova)**.

> We never ask for a private key, seed phrase, password or any payment, and we do not offer "fund recovery". Anyone asking for these in our name is not us.

**Not legal advice.** This is a technical record of public data. Victims should first file a complaint with the judicial authority, then with the cyber police ([policefata.ir](https://policefata.ir)).

---

<div dir="rtl">

## فارسی

### این مخزن چیست

سایت **[trace.avoxova.com](https://trace.avoxova.com)** گزارش عمومی یک پرونده‌ی فیشینگ در دامنه‌ی **dotomarket1.com** است. در آبان ۱۴۰۵ در این دامنه با عنوان فروش ارز DOTO پول جمع‌آوری شد. ایجنت هوشمند آوکسوا مسیر پول یک واریز ۱۰۰ تتری (BEP-20) را به‌صورت مستقل دنبال کرده است. این مسیر از شبکه‌ی بی‌ان‌بی (BSC) شروع می‌شود، از یک پل بین‌زنجیره‌ای می‌گذرد، به شبکه‌ی ریپل می‌رسد و در سرویس‌هایی تمام می‌شود که پول به آن‌ها رسیده است.

**این مخزن بخش باز و قابل‌بازتولید همان گزارش است.** هر عدد بلاکچینی که در سایت آمده، این‌جا در [`claims.json`](claims.json) ثبت شده است. کد [`verify.py`](verify.py) همه‌ی آن‌ها را مستقیم از نودهای عمومی بلاکچین دوباره بررسی می‌کند. لازم نیست به ما اعتماد کنید؛ خودتان اجرا کنید.

> این پرونده **فقط به دامنه‌ی dotomarket1.com** مربوط است و درباره‌ی خود توکن DOTO، صادرکننده‌ی آن یا هیچ سایت دیگری ادعایی ندارد. آمدن یک آدرس در این مخزن، بیان داده‌ی عمومی بلاکچین است و اتهامی به دارنده‌ی آن نیست. صرافی‌ها، امانت‌دارها و پل‌ها فقط به‌عنوان *مقصد* یا *زیرساخت* ذکر شده‌اند.

### چرا این مخزن را باز کردیم: دعوت از برنامه‌نویس‌ها

این مخزن برای برنامه‌نویس‌ها و تحلیلگران بلاکچین راه‌اندازی شده است تا بتوانند:

1. **بررسی کنند:** کد را اجرا کنند و اگر عددی نادرست بود، اطلاع بدهند.
2. **مسیر را کامل کنند:** پول را فراتر از جایی که ما رسیدیم دنبال کنند (کارهای باز را در پایین ببینید).
3. **روش را بهتر کنند:** بررسی‌ها را دقیق‌تر کنند، منبع اضافه کنند و بخش‌های استنباطی را کم کنند.

اصلاحیه‌ها حتی اگر خلاف نتیجه‌گیری ما باشند، پذیرفته می‌شوند. هر اصلاحیه‌ای که این‌جا تأیید شود، در سایت گزارش هم اعمال می‌شود.

### اجرا

فقط پایتون ۳.۹ به بالا و اینترنت لازم است. نصب بسته یا کلید API لازم نیست.

```bash
git clone https://github.com/avoxova/trace.git
cd trace
python3 verify.py
```

برای هر ادعا یکی از این نتایج نمایش داده می‌شود:
- تأیید شد: `PASS`
- رد شد: `FAIL`
- نیاز به نود آرشیوی دارد: `SKIP`

نتیجه‌ی فعلی روی نودهای عمومی رایگان: **۴۸ تأیید، ۰ رد، ۱ مورد نیازمند نود آرشیوی**.

### چه چیزهایی بررسی می‌شود

**در شبکه‌ی BSC:**
- واریز ۱۰۰ تتر، و جاروی آن دو دقیقه بعد (۹۵ تتر به کیف جمع‌آوری و ۵ تتر به معرف)
- همه‌ی گام‌های مسیرهای الف، ب و ج تا پل NEAR Intents
- مالک و خزانه‌ی قرارداد فروش

**در شبکه‌ی ریپل:**
- سه تبدیل تتر به ریپل و همه‌ی گام‌های میانی
- واریزها به Cobo (امانت‌دار دارایی) با چهار تگ
- واریزها به کیف مرتبط با MEXC

### کارهای باز برای کامل کردن مسیر

1. بررسی موجودی کیف جمع‌آوری درست پیش و پس از جارو، که به نود آرشیوی BSC نیاز دارد.
2. شمارش قابل‌بازتولید فرستنده‌ها و واریزهای کیف جمع‌آوری `0xe3df…988a` در ۲۶ تا ۳۰ آبان ۱۴۰۵.
3. ردیابی بقیه‌ی خروجی‌های کیف جمع‌آوری، فراتر از مسیرهای الف، ب و ج.
4. تأیید یا رد مسیر «احتمالی» ج. پیوند آن فعلاً از یک مجوز برداشت (approve) استنباط شده است.
5. دنبال کردن کیف مرتبط با MEXC و کیف تجمیع `r3GY…upLf`.

### مشارکت

- برای عدد نادرست، بررسی ردشده یا سرنخ تازه، **issue** باز کنید و هش تراکنش را هم بگذارید.
- ادعای تازه را با **pull request** به `claims.json` اضافه کنید و بررسی آن را هم در `verify.py` بنویسید.
- لطفاً داده‌ی شخصی، حدس درباره‌ی هویت افراد یا اتهام نفرستید و فقط به داده‌های بلاکچین بسنده کنید.

### ارتباط با ما

برای پرسش، اعلام خطا یا سرنخی که مناسب issue عمومی نیست، از راه تلگرام با **[@avoxova_support](https://t.me/avoxova_support)** در ارتباط باشید. خبرهای پرونده در کانال **[@avoxova](https://t.me/avoxova)** اعلام می‌شود.

> ما هرگز کلید خصوصی، عبارت بازیابی، رمز عبور یا هیچ وجهی درخواست نمی‌کنیم و خدمات «بازگرداندن وجه» نداریم؛ هر کس به نام ما چنین درخواستی کند، از طرف ما نیست.

**این مخزن مشاوره‌ی حقوقی نیست.** مال‌باختگان ابتدا به مرجع قضایی و سپس به پلیس فتا ([policefata.ir](https://policefata.ir)) مراجعه کنند.

</div>

---

**Report / گزارش:** [trace.avoxova.com](https://trace.avoxova.com) · [avoxova.com](https://avoxova.com) · [agent.avoxova.com](https://agent.avoxova.com) · [Telegram](https://t.me/avoxova) · [Support](https://t.me/avoxova_support) · [Instagram](https://www.instagram.com/avoxova/)
