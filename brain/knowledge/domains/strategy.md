# Purpose

تولید سیگنال معاملاتی. Strategy فقط سیگنال تولید می‌کند — اجرای سیگنال وظیفه Backtesting است (Separation of Alpha from Execution).

# Responsibilities

- تعریف فریمورک طراحی استراتژی (Strategy Framework)
- تولید سیگنال‌های معاملاتی (Buy/Sell/Hold)
- تعریف مدل `Signal` به‌عنوان خروجی استراتژی
- پشتیبانی از استراتژی‌های: Price Action، ICT، SMC، Volume Analysis، Order Flow

# Public Interfaces

- `Signal` (Entity) — سیگنال معاملاتی تولیدشده
- `Strategy` (Protocol/Interface) — قرارداد هر استراتژی
- `StrategyResult` (Value Object) — نتیجه اجرای استراتژی
- Events: `SignalGenerated`

# Dependencies

- از `market` استفاده می‌کند (داده ورودی استراتژی).
- از `shared_kernel` استفاده می‌کند.
- **هیچ وابستگی‌ای به `backtesting` ندارد** (ADR-0002).
- **هیچ وابستگی‌ای به `portfolio` یا `risk` ندارد**.

# Related ADRs

- ADR-0002 — Strategy Bounded Context است، نه Engine.

# Notes

- طبق ADR-0002، Strategy یک Bounded Context است نه Engine مستقل.
- Strategy نمی‌تواند order‌ها را اجرا کند — این وظیفه Backtesting است.
- در آینده امکان اضافه شدن Strategy Engine مستقل وجود دارد بدون نیاز به رفکتور Domain Model.