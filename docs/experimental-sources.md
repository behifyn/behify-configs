# منابع کانفیگ‌های آزمایشی

این سه کانفیگ مستقل از مجموعهٔ اصلی Behify هستند. در حال حاضر صرفاً تبدیل ساختاری/اعتبارسنجی شده‌اند و عملکرد اتصال‌شان تست نشده است.

| فایل Behify | منبع | مجوز | حداقل Xray-core |
| --- | --- | --- | --- |
| `behify-08-fraga.json` | [Patterniha fragA](https://github.com/patterniha/Serverless-for-Iran/blob/main/Serverless-fragA.jsonc) | GPL-3.0 | 26.6.27 |
| `behify-09-fragb.json` | [Patterniha fragB](https://github.com/patterniha/Serverless-for-Iran/blob/main/Serverless-fragB.jsonc) | GPL-3.0 | 26.6.27 |
| `behify-10-xtls.json` | [XTLS Serverless](https://github.com/XTLS/Xray-examples/blob/main/Serverless-for-Iran/serverless_for_Iran.jsonc) | CC BY-SA 4.0 | 25.12.8 |

## تغییرات نسبت به منبع

- کامنت‌های JSONC حذف شدند تا فایل JSON استاندارد قابل پردازش باشد.
- نام نمایشی با عنوان `Behify 08/09/10` جایگزین شد.
- تمام inboundها صریحاً به `127.0.0.1` محدود شدند تا پورت‌های محلی روی شبکه منتشر نشوند.
- تنظیمات لاگ روی `warning` و `dnsLog: false` قرار گرفت.
- متادیتای خارج از ساختار پیکربندی `__Credits__` در فایل‌های Patterniha حذف شد؛ انتساب منبع و مجوز در همین سند باقی است.
- به سایر پارامترهای DNS، Routing، Fragment و Noise دست زده نشده است.

نسخهٔ اصلی فایل‌ها با Git blob hash در `scripts/import_experimental.py` قفل شده است. واردکردن نسخهٔ جدید نیازمند بررسی و به‌روزرسانی آگاهانهٔ hashها است؛ اسکریپت در صورت تغییر upstream به‌جای تغییر بی‌سروصدای خروجی متوقف می‌شود.

کپی مجوزهای منابع همراه خروجی در `licenses/` نگهداری می‌شود. فایل‌های Patterniha به‌صورت تغییریافته تحت GPLv3 و فایل XTLS تحت CC BY-SA 4.0 بازنشر می‌شوند. این مجوزها تنها دربارهٔ محتوای اقتباس‌شده از آن منابع‌اند، نه لزوماً کل کد مستقل Behify.

کارکرد Runtime و سازگاری در v2rayNG و وضعیت شبکه هنوز تأیید نشده است. این کانفیگ‌ها اتصال مستقیم دارند و IP مقصد را از دید سرویس مقصد پنهان نمی‌کنند.
