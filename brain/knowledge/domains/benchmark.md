# Purpose

داده‌های بنچمارک مرجع (طلا، بیت‌کوین، CPI) برای مقایسه عملکرد پرتفوی. این context داده خام بنچمارک را نگهداری و ارائه می‌دهد.

# Responsibilities

- نگهداری داده‌های تاریخی بنچمارک‌ها
- تعریف مدل‌های دامنه‌ای بنچمارک (BenchmarkAsset، BenchmarkPrice)
- مدیریت لیست بنچمارک‌های فعال (Gold، Bitcoin، Real USD/CPI)
- ارائه داده بنچمارک به Portfolio Context برای مقایسه

# Public Interfaces

- `BenchmarkAsset` (Entity) — دارایی بنچمارک (طلا، بیت‌کوین و غیره)
- `BenchmarkPrice` (Entity) — قیمت بنچمارک در یک لحظه
- `BenchmarkType` (Value Object) — نوع بنچمارک (GOLD, BTC, REAL_USD)
- `BenchmarkRepository` (Port) — خواندن داده بنچمارک

# Dependencies

- از `shared_kernel` استفاده می‌کند.
- هیچ وابستگی به سایر bounded contextها ندارد.
- Portfolio از این context استفاده می‌کند (جهت مقایسه عملکرد).

# Related ADRs

- ADR-0001 — مقایسه بنچمارک بر اساس TWR انجام می‌شود.

# Notes

- در MVP سه بنچمارک پشتیبانی می‌شود: طلا (Gold)، بیت‌کوین (Bitcoin)، دلار واقعی تعدیل‌شده با تورم آمریکا (Real USD / CPI-adjusted).
- Real USD نیاز به داده CPI دارد (از FRED API یا منبع مشابه).
- بنچمارک‌ها باید قابلیت اضافه شدن بدون تغییر Core را داشته باشند (Plugin Architecture).