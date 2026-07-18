# ADR-0001: Time-Weighted Return (TWR) Metric

## Status

Approved

## Date

2026-07-14

## Context

Prism Intelligence نیاز به یک معیار اصلی برای اندازه‌گیری عملکرد پرتفوی دارد. هدف اصلی پروژه — پاسخ به این سوال که «آیا سرمایه‌گذار واقعاً در حال خلق ثروت است یا صرفاً از رشد اسمی بازار و ورود سرمایه جدید بهره می‌برد؟» — نیازمند معیاری است که اثر ورود و خروج سرمایه را حذف کند.

گزینه‌های موجود:
- **Time-Weighted Return (TWR):** اثر cash flowهای خارجی را حذف می‌کند.
- **Money-Weighted Return (MWR / IRR):** زمان‌بندی cash flowها را در نظر می‌گیرد.
- **Simple Return:** بدون تعدیل، مناسب نیست.

## Decision

معیار اصلی عملکرد پرتفوی **Time-Weighted Return (TWR)** است.

**Fallback:** **Modified Dietz** فقط زمانی استفاده می‌شود که timestamp دقیق cash flowها در دسترس نباشد.

## Consequences

- Portfolio Engine باید NAV snapshots را در اطراف رویدادهای cash flow ذخیره کند.
- مقایسه بنچمارک‌ها بر اساس TWR انجام می‌شود.
- Attribution analysis از بازده مبتنی بر TWR استفاده می‌کند.
- MWR به‌عنوان معیار مکمل محاسبه می‌شود، نه جایگزین.

## Alternatives

- **MWR به‌عنوان معیار اصلی:** رد شد چون MWR به زمان‌بندی واریز/برداشت وابسته است و عملکرد واقعی فرآیند سرمایه‌گذاری را نشان نمی‌دهد.
- **Simple Return:** رد شد چون اثر cash flowها را نادیده می‌گیرد و گمراه‌کننده است.

## References

- Master Document — Vision section
- Architecture v1 — معیارهای عملکردی اصلی