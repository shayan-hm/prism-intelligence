# Purpose

محاسبه NAV، حسابداری پوزیشن و وجه نقد، و مقایسه عملکرد پرتفوی با بنچمارک‌های مرجع.

# Responsibilities

- محاسبه NAV (Net Asset Value) بر اساس TWR (معیار اصلی، ADR-0001)
- محاسبه MWR به‌عنوان معیار مکمل
- حسابداری پوزیشن‌های باز و بسته‌شده
- حسابداری وجه نقد (Cash)
- مقایسه عملکرد با بنچمارک‌ها: طلا، بیت‌کوین، دلار واقعی تعدیل‌شده با CPI
- محاسبه Real USD Return
- Attribution Analysis (ساده‌شده در MVP، Full Brinson در فازهای بعدی)
- ارزیابی فصلی (Quarterly Evaluation)

# Public Interfaces

- `Portfolio` (Entity) — پرتفوی با پوزیشن‌ها و وجه نقد
- `Position` (Entity) — پوزیشن باز در یک نماد
- `NAVSnapshot` (Entity) — snapshot NAV در یک لحظه
- `PortfolioService` (Domain Service) — محاسبه NAV و بازده
- Events: `NAVUpdated`، `PositionOpened`، `PositionClosed`، `CashDeposited`، `CashWithdrawn`

# Dependencies

- از `market` استفاده می‌کند (قیمت لحظه‌ای برای محاسبه NAV).
- از `benchmark` استفاده می‌کند (داده بنچمارک برای مقایسه).
- از `shared_kernel` استفاده می‌کند.
- **تولید سیگنال معاملاتی ممنوع است** — این وظیفه Strategy است.

# Related ADRs

- ADR-0001 — TWR معیار اصلی عملکرد است.
- ADR-0002 — Portfolio Agent نباید سیگنال تولید کند.

# Notes

- Portfolio & NAV یک Engine مستقل است.
- NAV snapshots باید در اطراف رویدادهای cash flow ذخیره شوند (جهت محاسبه صحیح TWR).
- Portfolio Agent فقط اجازه پیاده‌سازی NAV، حسابداری پوزیشن و مقایسه بنچمارک را دارد.