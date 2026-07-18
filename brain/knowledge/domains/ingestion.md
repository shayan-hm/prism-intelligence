# Purpose

جمع‌آوری، اعتبارسنجی، نرمال‌سازی و ذخیره داده‌های بازار از providerهای مختلف. این context مسئول pipeline ورود داده است.

# Responsibilities

- جمع‌آوری داده خام از providerهای بازار (Yahoo Finance و آینده)
- اعتبارسنجی داده (Completeness، Consistency، Range checks)
- نرمال‌سازی فرمت providerها به مدل یکپارچه (Canonical)
- شناسایی و گزارش شکاف داده (Data Gap Detection)
- ذخیره داده در لایه Infrastructure

# Public Interfaces

- `IngestionService` (Domain Service) — هماهنگی pipeline ورود داده
- `DataValidator` (Domain Service) — اعتبارسنجی داده
- `DataNormalizer` (Domain Service) — نرمال‌سازی به مدل یکپارچه
- Events: `DataIngested`، `DataValidationError`، `DataGapDetected`

# Dependencies

- از `market` استفاده می‌کند (مدل‌های Candle، Symbol، Timeframe).
- از `shared_kernel` استفاده می‌کند.
- Contextهای دیگر به این context وابستگی ندارند.

# Related ADRs

- مستقیم به ADR خاصی وابسته نیست، اما پایه Phase 2 است.

# Notes

- Ingestion یک Engine مستقل است (نه فقط Bounded Context).
- Provider adapterها در `infrastructure/market_data/adapters/` قرار دارند.
- در MVP فقط فارکس با تایم‌فریم 1m پشتیبانی می‌شود. تایم‌فریم‌های بالاتر (5m, 15m, 1h, 4h, D1) از 1m ساخته می‌شوند.