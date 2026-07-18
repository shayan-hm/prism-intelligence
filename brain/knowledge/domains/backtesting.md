# Purpose

شبیه‌سازی اجرای استراتژی روی داده‌های تاریخی و محاسبه معیارهای عملکرد. Backtesting اجرای سیگنال‌های Strategy را شبیه‌سازی می‌کند.

# Responsibilities

- شبیه‌سازی اجرای سیگنال‌های Strategy روی داده تاریخی
- محاسبه معیارهای عملکرد: PnL، Drawdown، Win Rate، Sharpe Ratio
- شبیه‌سازی order execution (Market/Limit/Stop)
- مدیریت فرضیات شبیه‌سازی (slippage، spread، commission)
- تولید گزارش نتایج بک‌تست

# Public Interfaces

- `BacktestService` (Domain Service) — اجرای شبیه‌سازی
- `BacktestResult` (Entity) — نتیجه کامل بک‌تست
- `TradeRecord` (Entity) — رکورد هر معامله شبیه‌سازی‌شده
- `PerformanceMetrics` (Value Object) — PnL، Drawdown، Win Rate، Sharpe Ratio
- Events: `BacktestCompleted`، `BacktestFailed`

# Dependencies

- از `market` استفاده می‌کند (داده تاریخی).
- سیگنال‌های `strategy` را مصرف می‌کند.
- از `shared_kernel` استفاده می‌کند.

# Related ADRs

- ADR-0002 — Separation of Alpha from Execution.

# Notes

- Backtesting یک Engine مستقل است.
- شبیه‌سازی باید فرضیات خود را صریحاً مستند کند (slippage model، spread assumption، commission structure).
- Backtest Agent مجاز است فقط در این context کار کند.