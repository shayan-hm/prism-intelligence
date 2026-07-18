# Purpose

مدیریت داده‌های بازار (قیمت، حجم، تایم‌فریم) و ارائه داده خام به سایر Bounded Contextها. این context هیچ منطق تحلیلی ندارد — صرفاً داده را نگهداری و ارائه می‌دهد.

# Responsibilities

- تعریف مدل‌های دامنه‌ای داده بازار (Candle/OHLCV، Tick، Symbol، Timeframe)
- نگهداری و ارائه داده خام به Contextهای مصرف‌کننده (Ingestion، Backtesting، Strategy)
- تعریف قرارداد (Port) برای دسترسی به داده بازار

# Public Interfaces

- `MarketDataRepository` (Port) — خواندن داده بازار بر اساس symbol، timeframe، بازه زمانی
- `Symbol` (Entity) — نماد معاملاتی
- `Candle` (Entity) — شمع OHLCV
- `Timeframe` (Value Object) — تایم‌فریم (1m, 5m, 15m, 1h, 4h, D1)
- `Price` (Value Object) — قیمت با precision و currency

# Dependencies

- فقط از `shared_kernel` استفاده می‌کند.
- هیچ وابستگی به سایر bounded contextها ندارد.

# Related ADRs

- ADR-0001 (TWR) — داده بازار پایه محاسبه بازده است.

# Notes

- پیاده‌سازی واقعی دریافت داده (از Yahoo Finance و غیره) در `infrastructure/market_data/` و `ingestion` context قرار دارد.
- در MVP فقط فارکس پشتیبانی می‌شود.