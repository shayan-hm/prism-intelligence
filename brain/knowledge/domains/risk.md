# Purpose

کنترل ریسک، محاسبه exposure، و enforce محدودیت‌های ریسک روی پرتفوی. منطق ریسک مستقل از تولید سیگنال است.

# Responsibilities

- محاسبه Position Sizing
- محاسبه Exposure (نسبت سرمایه درگیر به کل سرمایه)
- محاسبه Drawdown (از peak)
- Enforce محدودیت‌های ریسک (Risk Limits)
- بررسی Leverage
- بررسی Concentration (تمرکز روی یک نماد یا بخش)
- محاسبه معیارهای ریسک

# Public Interfaces

- `RiskPolicy` (Entity) — سیاست ریسک تعریف‌شده برای پرتفوی
- `RiskAssessment` (Value Object) — نتیجه ارزیابی ریسک
- `PositionSize` (Value Object) — اندازه پیشنهادی پوزیشن
- `RiskService` (Domain Service) — ارزیابی و enforce ریسک
- Events: `RiskLimitBreached`، `RiskAssessmentCompleted`

# Dependencies

- از `portfolio` استفاده می‌کند (داده پوزیشن و NAV).
- از `market` استفاده می‌کند (داده قیمت برای محاسبه exposure).
- از `shared_kernel` استفاده می‌کند.
- **تولید سیگنال معاملاتی ممنوع است** — این وظیفه Strategy است.

# Related ADRs

- ADR-0002 — Risk Agent نباید سیگنال تولید کند.

# Notes

- Risk Management یک Engine مستقل است.
- منطق ریسک باید مستقل از تولید سیگنال باشد — Risk فقط بررسی و محدود می‌کند.
- Risk Agent فقط در این context کار می‌کند.