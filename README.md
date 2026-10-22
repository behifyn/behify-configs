# Behify Configs

کانفیگ‌های Xray مربوط به Behify رو اینجا نگه می‌داریم تا برای دریافت تغییرات بعدی لازم نباشه فایل جدید رو هر بار دستی وارد کنید.

این‌ها بیشتر **اتصال مستقیم با Fragment** هستن، نه سرور VPN. آی‌پی شما رو تغییر نمی‌دن و ممکنه روی یک اینترنت جواب بدن، روی یکی دیگه نه.

## لینک‌ها

**نسخهٔ اصلی — ۷ کانفیگ**

```text
https://raw.githubusercontent.com/behifyn/behify-configs/main/sub/v2rayng.json
```

**نسخهٔ آزمایشی — ۳ کانفیگ جدید**

```text
https://raw.githubusercontent.com/behifyn/behify-configs/main/sub/experimental-v2rayng.json
```

آدرس رو در بخش Subscription برنامهٔ **v2rayNG** اضافه کنید و Update subscription بزنید. بعداً هم همین آدرس رو آپدیت می‌کنیم. وارد شدن این آرایهٔ JSON و اجرای جزئیاتش به نسخهٔ برنامه و هستهٔ Xray بستگی داره؛ تست واقعی هنوز لازمه.

**Hiddify:** این فایل‌ها Xray JSON هستن و خروجی معادل و تست‌شده‌ای برای sing-box/Hiddify نداریم.

## چی توی مخزنه؟

- `profiles/` — هفت کانفیگ اصلی؛ دست‌نخورده
- `experimental/` — سه نمونهٔ آزمایشی: دو نسخه از Patterniha و یکی از مثال‌های XTLS
- `sub/` — لینک‌های اشتراک اصلی و آزمایشی
- `scripts/build.py` — ساخت خروجی‌ها و بررسی خطاهای ساختاری
- `scripts/import_experimental.py` — دریافت نسخهٔ بررسی‌شدهٔ منابع و تبدیل JSONC به JSON
- `docs/experimental-sources.md` و `licenses/` — منبع، تغییرات و مجوز بازنشر

## به‌روزرسانی

اگه فقط کانفیگی رو ویرایش کردی:

```bash
python scripts/build.py
python scripts/build.py --check
```

اگه فایل‌های جدید آزمایشی هنوز دانلود نشده‌اند، یک‌بار قبل از دستورهای بالا اجرا کن:

```bash
python scripts/import_experimental.py
```

دانلود منابع روی نسخهٔ مشخصی قفل شده؛ اگه upstream تغییر کنه، اسکریپت خودسرانه فایل جدید رو جایگزین نمی‌کنه. بعد از بررسی تغییرات، فایل‌های `experimental/` و خروجی `sub/experimental-v2rayng.json` و پوشهٔ `licenses/` رو هم commit کن.

## قبل از تست

- دو پروفایل Patterniha به حداقل Xray-core `26.6.27` نیاز دارن؛ نمونهٔ XTLS حداقل `25.12.8` رو اعلام کرده.
- آزمایشی‌ها الزاماً بهتر از کانفیگ‌های قبلی نیستن. روی اینترنت و دستگاه خودت مقایسه‌شون کن.
- در بعضی پروفایل‌های اصلی مسیر تلگرام از یک SOCKS خارجی استفاده می‌کنه؛ محرمانگی و پایداری اون سرور تضمین‌شده نیست.
- JSON معتبر به‌معنی اتصال موفق نیست و بررسی این مخزن روی GitHub هم تست شبکهٔ ایران نیست.

برای گزارش مشکل، می‌تونی [Issue](https://github.com/behifyn/behify-configs/issues) باز کنی. اسم اپ، نسخه و نوع اینترنت کافیه؛ اطلاعات شخصی یا حساب نفرست.

منبع کانفیگ‌های جدید و شرایط استفاده‌شون در [این فایل](docs/experimental-sources.md) ثبت شده.
