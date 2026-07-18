# Architecture v1 — Prism Intelligence

**نسخه:** 1.0 — بازطراحی کامل بعد از بررسی Notion workspace (اکنون منتقل‌شده به `brain/`)
**تاریخ:** 2026-07-14
**تکنولوژی:** Python 3.12+ · FastAPI · PostgreSQL · Docker
**الگو:** Clean Architecture (Ports & Adapters) + Lightweight DDD + Plugin Architecture

> منبع: این فایل از سند "Prism Intelligence — Master Document" (فارسی، ژوئیهٔ ۲۰۲۶) منتقل شده است. هر تغییر بعدی در این فایل باید طبق قوانین `brain/system/governance.md` مستند شود.

## Bounded Contexts هسته‌ای

۱. `shared_kernel`
۲. `market`
۳. `ingestion`
۴. `strategy`
۵. `backtesting`
۶. `benchmark`
۷. `portfolio`
۸. `risk`

## Engineهای مستقل

- Ingestion Engine
- Backtesting Engine
- Portfolio & NAV Engine
- Risk Management Engine

**قید صریح:** تعداد engineها محدود به همین چهار مورد است (constraint معماری شایان). Strategy یک Bounded Context است، نه یک engine پنجم — دلیل این تصمیم در ADR-0002 مستند شده.

## اصل معماری کلیدی

**Separation of Alpha from Execution** — تولید سیگنال در `strategy` و شبیه‌سازی اجرا در `backtesting` کاملاً از هم جدا هستند. `strategy` هیچ وابستگی‌ای به `backtesting` ندارد.

## ساختار لایه‌ها

- Layer 1: Domain
- Layer 2: Application
- Layer 3a: Infrastructure
- Layer 3b: Markets
- Layer 4: Interfaces

## معیارهای عملکردی اصلی

- Time-Weighted Return (TWR) — معیار اصلی، طبق ADR-0001
- Money-Weighted Return (MWR) — معیار مکمل
- Real USD Return (تعدیل‌شده با CPI)
- Benchmark Comparison (Gold / Bitcoin / Real USD)
- Attribution Analysis

## قوانین Dependency (اجباری، enforced توسط `.importlinter`)

- وابستگی‌ها همیشه به سمت داخل (به سمت Domain) هستند.
- `domain` هیچ import خارجی ندارد.
- `application` فقط از طریق Ports به لایه‌های بیرونی وابسته است.
- Market pluginها به همدیگر import ندارند.
- فقط `container.py` (در صورت وجود) می‌تواند از تمام لایه‌ها import کند.

جزئیات فنی این قوانین در فایل `.importlinter` ریشهٔ ریپو تعریف شده‌اند — این فایل معتبرترین منبع برای enforcement است. این سند فقط خلاصهٔ مفهومی است.

## Quality Enforcement

- `import-linter` برای enforcement قوانین dependency
- Unit test برای Domain و Application
- Integration test برای Infrastructure
- E2E test برای API

## محدودهٔ MVP

### شامل
- فارکس (Forex)
- Ingestion
- Backtesting
- Strategy Framework
- Portfolio & NAV
- Risk
- Benchmark Comparison
- REST API

### خارج از محدوده (فازهای بعدی)
- اجرای واقعی معامله (real trade execution)
- بازارهای غیر-Forex (Crypto، Stocks، Iran Market، Options، Commodity/Energy)
- Dashboard UI
- Multi-tenancy
- Full Brinson attribution

## معیار موفقیت معماری

اگر یک بازار، استراتژی، یا benchmark جدید بتواند صرفاً با ایجاد فایل‌های جدید (بدون تغییر در Core) اضافه شود، معماری موفق تلقی می‌شود. این یک تست عملی است که باید قبل از هر ادعای "معماری کامل شد" بررسی شود — نه یک شعار.

## مرجع فایل‌های مرتبط در ریپو

- `.importlinter` — قوانین enforced dependency
- `OPENCODE.md` — قوانین کدنویسی برای OpenCode
- `docs/agents/*.md` — نقش و محدودیت هر sub-agent (ingestion, backtest, portfolio, risk)
- `brain/knowledge/decisions/` — ADRهای کامل
