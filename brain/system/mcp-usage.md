# استفاده از MCP برای دسترسی به Brain

## نوع سرور

یک سرور MCP عمومی filesystem/git، متصل به مسیر ریشهٔ ریپوی `prism-intelligence` (یا حداقل شامل مسیر `brain/`). این سرور enforcement داخلی ندارد — فقط read/write/git operations خام فراهم می‌کند. تمام قوانین (`governance.md`) صرفاً از طریق instruction به هر AI اجرا می‌شوند، نه از طریق کد سرور.

## کانفیگ نمونه (Claude Desktop / سرورهای سازگار با MCP config استاندارد)

از سرور رسمی filesystem و در صورت نیاز git استفاده کنید. نمونه:

```json
{
  "mcpServers": {
    "prism-brain-fs": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/absolute/path/to/prism-intelligence"
      ]
    },
    "prism-brain-git": {
      "command": "uvx",
      "args": [
        "mcp-server-git",
        "--repository",
        "/absolute/path/to/prism-intelligence"
      ]
    }
  }
}
```

- `server-filesystem` برای خواندن/نوشتن فایل‌های `brain/`.
- `mcp-server-git` برای commit جداگانه (طبق قانون commit) — این سرور امکان `git add`, `git commit`, `git log`, `git diff` را از طریق MCP فراهم می‌کند.

**نکته:** مسیر باید به ریشهٔ ریپو اشاره کند (نه فقط `brain/`)، چون commit جدا برای کد نیز از همین سرور انجام می‌شود.

## Instruction اجباری که باید در system prompt / project instructions هر AI درج شود

این متن (یا معادل انگلیسی آن) باید در تنظیمات هر سه AI (Claude Project Instructions، ChatGPT Custom Instructions/System Prompt، OpenCode config) قرار گیرد:

```
قبل از هر کاری روی پروژهٔ Prism Intelligence، فایل‌های زیر را از طریق MCP بخوان:
1. brain/README.md
2. brain/system/governance.md
3. brain/knowledge/architecture/architecture-v1.md
4. تمام فایل‌های brain/knowledge/decisions/ با Status = Approved

هنگام نوشتن در brain/:
- هر ADR جدید باید Status: Proposed داشته باشد مگر کاربر صراحتاً تایید کند.
- هرگز فایل موجود در knowledge/decisions/ را حذف یا overwrite نکن؛ به‌جایش ADR جدید بساز که ارجاع بدهد.
- هر commit که brain/ را تغییر می‌دهد باید commit جداگانه با پیام شروع‌شده با "brain:" باشد، کاملاً جدا از commit تغییرات کد.
```

## نکات عملیاتی

- **بدون concurrency control خودکار:** اگر بیش از یک AI هم‌زمان روی یک فایل کار کند، مسئولیت هماهنگی با کاربر است (طبق تصمیم گرفته‌شده در طراحی اولیه).
- **بدون PR/review اجباری:** commitها مستقیم روی برنچ `main` می‌روند. این یعنی audit فقط از طریق `git log --grep="^brain:"` یا بررسی دوره‌ای توسط کاربر ممکن است، نه از طریق gate خودکار.
- **بررسی دوره‌ای پیشنهادی (نه اجباری):** کاربر می‌تواند به‌صورت دوره‌ای با `git log --oneline --grep="^brain:"` تغییرات brain را مرور کند تا از انباشته‌شدن تصمیمات نادیده‌گرفته‌شده جلوگیری شود.
