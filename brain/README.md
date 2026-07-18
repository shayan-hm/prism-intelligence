# Prism Intelligence — Brain

## این فولدر چیست

این فولدر تنها منبع truth دانش، معماری، و تصمیمات پروژهٔ Prism Intelligence است.

Notion **دیگر استفاده نمی‌شود**. هر اطلاعاتی که قبلاً در Notion بود (architecture، roadmap، ADRها) به این فولدر منتقل شده یا در حال انتقال است. اگر تناقضی بین این فولدر و Notion دیدی، این فولدر (`brain/`) معتبر است.

## قانون اول برای هر AI (کلاد، ChatGPT، OpenCode)

**قبل از هر کاری، این فایل‌ها را به همین ترتیب بخوان:**

1. `brain/README.md` (همین فایل)
2. `brain/system/governance.md` — قوانین نوشتن، commit، و دسترسی
3. `brain/knowledge/architecture/architecture-v1.md` — معماری فعلی پروژه
4. `brain/knowledge/decisions/` — تمام ADRها (به ترتیب شماره)
5. `brain/knowledge/domains/` — فایل مربوط به bounded context‌ای که روی آن کار می‌کنی

بدون خواندن این‌ها، هیچ تصمیم معماری یا تغییر کد نباید گرفته شود.

## ساختار فولدرها

| فولدر | محتوا | چه کسی می‌نویسد |
|---|---|---|
| `system/` | قوانین حاکم بر خود brain (governance، نحوهٔ استفاده از MCP) | فقط انسان (شایان) ادیت می‌کند؛ AIها فقط می‌خوانند |
| `knowledge/architecture/` | معماری فعلی و تاریخچهٔ تغییرات معماری | AIها می‌نویسند، ولی هر تغییر باید ابتدا به‌عنوان ADR ثبت شود |
| `knowledge/decisions/` | ADRها — تصمیمات معماری/فنی مستند و غیرقابل‌بازگشت بدون ADR جدید | AIها می‌نویسند طبق `_template.md` |
| `knowledge/domains/` | دانش هر bounded context (portfolio, market, ingestion, backtesting, risk, strategy, benchmark) | AIها می‌نویسند و به‌روزرسانی می‌کنند |
| `knowledge/research/` | یافته‌های تحقیقاتی (از Gemini، Perplexity، یا هر منبع) — غیر رسمی، هنوز ADR نشده | AIها می‌نویسند آزادانه |
| `agents/` | نقش و ارجاع هر AI — محتوای واقعی رفتار AIها همچنان در `docs/agents/*.md` است | فقط ارجاع، نه تکرار محتوا |
| `contexts/` | خلاصهٔ context بین جلسات (اختیاری، در صورت نیاز) | AIها می‌نویسند |
| `experiments/` | ایده‌های آزمایشی که هنوز تصمیم قطعی نشده‌اند — پیش‌نویس ADR | AIها می‌نویسند آزادانه |

## قانون Commit (اجباری — بدون استثنا)

هر تغییر در `brain/` باید این دو قاعده را رعایت کند:

1. **پیشوند commit**: هر commit که فایلی داخل `brain/` را تغییر می‌دهد باید با `brain:` شروع شود.
   مثال: `brain: adr-0003 اضافه شد - تصمیم benchmark rebalancing`

2. **Commit جدا**: حتی اگر همان لحظه کد هم تغییر کرده، تغییرات `brain/` باید در یک commit جداگانه از تغییرات کد باشد. هرگز `brain/` و `src/` در یک commit مخلوط نشوند.

این قانون برای audit است — شایان باید بتواند با `git log --oneline --grep="^brain:"` کل تاریخچهٔ تصمیمات را جدا از تاریخچهٔ کد ببیند.

## دسترسی

هر سه AI (Claude، ChatGPT، OpenCode) هم می‌توانند بخوانند و هم بنویسند. محدودیت دسترسی per-folder یا per-AI فعلاً وجود ندارد — طبق تصمیم صریح شایان. این یعنی کنترل کیفیت صرفاً از طریق رعایت این README و governance.md توسط خود AIها انجام می‌شود، نه از طریق enforcement فنی.
