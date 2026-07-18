# استفاده از MCP برای دسترسی به Brain

## نوع سرور

دو گزینه برای دسترسی به Brain وجود دارد:

### ۱. سرور MCP اختصاصی `tools/brain` (توصیه‌شده)

ابزار `tools/brain` یک MCP Server اختصاصی برای Prism Intelligence است که بخشی از قوانین governance را به‌صورت برنامه‌ای enforce می‌کند.

**امکانات:**
- ۱۴ ابزار MCP (خواندن، جستجو، ایجاد، ویرایش، حذف، جابجایی، patch اسناد + عملیات git)
- Path traversal protection
- محدودیت فایل به `.md`
- Enforcement خودکار prefix `brain:` در commit

**نصب و اجرا:**
```bash
cd tools/brain
pip install -e .
python -m brain.mcp.server
```

**ابزارهای ثبت‌شده:**
- `read_brain`، `search_brain`، `get_context`، `list_documents`
- `create_document`، `update_document`، `append_document`، `delete_document`، `move_document`، `apply_patch`
- `git_status`، `git_diff`، `git_log`، `git_commit`

### ۲. سرورهای MCP عمومی (fallback)

اگر سرور اختصاصی در دسترس نبود، از سرورهای عمومی استفاده کنید:

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

**هشدار:** سرورهای عمومی هیچ enforcement داخلی ندارند — تمام قوانین باید صرفاً از طریق instruction به AIها اجرا شوند.

## Instruction اجباری که باید در system prompt هر AI درج شود

این متن (یا معادل انگلیسی آن) باید در تنظیمات هر AI قرار گیرد:

```
قبل از هر کاری روی پروژه Prism Intelligence، فایل‌های زیر را بخوان:
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

- **بدون concurrency control خودکار:** اگر بیش از یک AI هم‌زمان روی یک فایل کار کند، مسئولیت هماهنگی با کاربر است.
- **بدون PR/review اجباری:** commitها مستقیم روی برنچ `main` می‌روند.
- **بررسی دوره‌ای:** با `git log --oneline --grep="^brain:"` تغییرات brain را مرور کنید.