# ADR-0002: Strategy as Bounded Context

## Status

Approved

## Date

2026-07-14

## Context

در طراحی اولیه، سوال مطرح بود که آیا Strategy باید یک Engine مستقل (مانند Ingestion، Backtesting، Portfolio، Risk) باشد یا یک Bounded Context درون Domain Layer.

اگر Strategy یک Engine مستقل باشد:
- مزیت: استقلال کامل و deploy جداگانه
- معایب: تعداد engineها از ۴ به ۵ افزایش می‌یابد (ناقض constraint معماری)، پیچیدگی deployment

اگر Strategy یک Bounded Context باشد:
- مزیت: تعداد engineها محدود به ۴ می‌ماند، سادگی معماری
- معایب: با Backtesting coupling مفهومی دارد (ولی نه فنی)

## Decision

Strategy به‌عنوان یک **Bounded Context** پیاده‌سازی می‌شود، نه یک Engine مستقل.

## Consequences

- Strategy فقط `Signal` objects تولید می‌کند.
- Backtesting Engine سیگنال‌های Strategy را مصرف و اجرا را شبیه‌سازی می‌کند.
- Strategy هیچ وابستگی‌ای به Backtesting ندارد (Separation of Alpha from Execution).
- در آینده اگر لازم باشد، یک Strategy Engine جداگانه بدون رفکتور Domain Model می‌تواند اضافه شود.
- تعداد Engineهای مستقل محدود به ۴ می‌ماند: Ingestion، Backtesting، Portfolio & NAV، Risk Management.

## Alternatives

- **Strategy Engine پنجم:** رد شد — constraint شایان مبنی بر حداکثر ۴ engine.
- **ادغام Strategy در Backtesting:** رد شد — اصل Separation of Alpha from Execution نقض می‌شد.

## References

- Master Document — Architecture section
- Architecture v1 — Engineهای مستقل