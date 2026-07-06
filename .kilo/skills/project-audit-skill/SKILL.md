---
name: project-audit
version: 2.0.0
description: |
  بررسی کامل repository یک پروژه (کد + config + مستندات) در برابر استانداردهای داخلی شرکت و تولید گزارش Markdown انطباق + راهنمای رفع نقص.
  پشتیبانی از GitLab و Local filesystem. برای پروژه‌های بزرگ، progress ذخیره می‌شود تا در session جدید ادامه داد.

  این skill را حتماً فعال کن وقتی:
  - کاربر بخواهد پروژه‌ای را "بررسی"، "ممیزی" یا "audit" کند
  - کاربر بپرسد "آیا پروژه با استانداردهای شرکت تطابق دارد؟"
  - کاربر از "compliance"، "production readiness"، "project quality" صحبت کند
  - کاربر بگوید "ادامه audit" یا "continue" برای از سرگیری session قبلی

changelog:
  v2.0.0:
    - اضافه شدن حوزه ARCH (معماری و مقیاس‌پذیری) — وزن 10
    - اضافه شدن حوزه RESILIENCE (پایداری و DRP) — وزن 10
    - اضافه شدن حوزه CICD (containerization، مات) — وزن 5
    - گسترش OBS: NTP sync، gateway sample-rate، health check با وابستگی‌ها، alert rule
    - گسترش SEC-DB: replication، ایندکس با مشورت DB team
    - گسترش SEC-APP: audit trail operators، env isolation
    - گسترش API: breaking change validation، error catalog
    - وزن‌بندی کلی بازبینی شد (جمع همچنان 100)
---

# Project Audit Skill — v2.0

بررسی کامل پروژه (کد + config + مستندات) در برابر استانداردهای داخلی شرکت.

**خروجی‌ها (هر دو Markdown):**
1. `audit-report.md` — گزارش انطباق با امتیازدهی
2. `remediation-guide.md` — راهنمای عملی و کد-محور رفع نقص‌ها

---

## گام ۰ — بررسی Session قبلی

**ابتدا** بررسی کن آیا `audit-progress.json` وجود دارد:

```bash
cat {output_dir}/audit-progress.json 2>/dev/null || echo "NOT_FOUND"
cat {repo_path}/audit-output/audit-progress.json 2>/dev/null || echo "NOT_FOUND"
```

- **وجود دارد** → از `pending_checks` ادامه بده، نتایج قبلی را نگه‌دار
- **وجود ندارد** → session جدید شروع کن

---

## گام ۱ — دریافت ورودی‌ها

اگر کاربر مشخص نکرده، بپرس:

| پارامتر | پیش‌فرض | توضیح |
|---------|---------|-------|
| `repo_source` | — | GitLab URL یا مسیر local |
| `lang` | auto-detect | Python / Node.js / Go / Java |
| `output_dir` | `{repo_path}/audit-output/` | محل ذخیره گزارش‌ها |
| `checks_scope` | all | لیست checks (پیش‌فرض: همه) |
| `project_type` | commercial | commercial / mvp / banking — روی وزن‌دهی اثر می‌گذارد |

### دسترسی به Repository

**Local filesystem:**
```bash
ls -la {repo_path}
```

**GitLab (با token):**
```bash
git clone https://oauth2:{GITLAB_TOKEN}@{gitlab_url}/{group}/{project}.git /tmp/audit_repo
```

---

## گام ۲ — شناسایی Tech Stack

```bash
find {repo_path} -maxdepth 4 -type f \( \
  -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.go" \
  -o -name "*.java" -o -name "requirements*.txt" \
  -o -name "package.json" -o -name "go.mod" -o -name "pom.xml" \
  -o -name "Dockerfile*" -o -name "docker-compose*" \
  -o -name "*.yaml" -o -name "*.yml" -o -name ".env*" \
  \) 2>/dev/null | grep -v node_modules | grep -v ".git" | head -150

cat {repo_path}/package.json 2>/dev/null | python3 -c \
  "import json,sys; d=json.load(sys.stdin); print(list(d.get('dependencies',{}).keys())[:15])"
head -20 {repo_path}/requirements.txt 2>/dev/null
cat {repo_path}/go.mod 2>/dev/null | head -10
```

---

## گام ۳ — اجرای Checks

→ جزئیات کامل هر check در `references/checks.md`

**ترتیب اجرا (از پر-وزن به کم‌وزن):**

| شناسه | حوزه | وزن | جدید در v2؟ |
|-------|------|-----|-------------|
| `observability` | OpenTelemetry + SigNoz + Health check + Alert | 20 | گسترش یافت |
| `logging` | Structured Logging + requestId + masking | 15 | کاهش وزن |
| `security_network` | HTTPS + Rate Limit + Secrets + CORS | 10 | کاهش وزن |
| `security_database` | SQL Injection + env vars + backup + replication | 10 | گسترش یافت |
| `security_app` | Auth + hashing + validation + env isolation | 10 | گسترش یافت |
| `arch` | معماری + مقیاس‌پذیری + abstraction + DI | 10 | **جدید** |
| `resilience` | DRP + تست فشار + circuit breaker + error catalog | 10 | **جدید** |
| `business_reporting` | Queue-based events + schema | 5 | بدون تغییر |
| `api_standards` | OpenAPI + versioning + breaking change | 5 | گسترش یافت |
| `cicd` | Containerization + مات standard + CI pipeline | 5 | **جدید** |

> **نکته project_type:** برای پروژه‌های `banking`، وزن `resilience` و `observability` ۵ امتیاز اضافی دارند (از `cicd` و `business_reporting` کسر می‌شود).

**برای هر check:**
1. دستورات bash از `references/checks.md` را اجرا کن
2. نتیجه را ارزیابی کن (امتیاز ۰-۱۰۰)
3. progress را ذخیره کن

---

## گام ۴ — ذخیره Progress

```python
import json, datetime, pathlib

pathlib.Path("{output_dir}").mkdir(parents=True, exist_ok=True)
progress_file = "{output_dir}/audit-progress.json"

try:
    progress = json.load(open(progress_file))
except:
    progress = {
        "session_id": datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),
        "repo_path": "{repo_path}",
        "output_dir": "{output_dir}",
        "lang": "{detected_lang}",
        "project_type": "{project_type}",
        "completed_checks": [],
        "pending_checks": [
            "observability","logging","security_network",
            "security_database","security_app",
            "arch","resilience",
            "business_reporting","api_standards","cicd"
        ],
        "partial_results": {},
        "scores": {},
        "last_updated": ""
    }

check_name = "{current_check}"
progress["completed_checks"].append(check_name)
progress["pending_checks"] = [c for c in progress["pending_checks"] if c != check_name]
progress["partial_results"][check_name] = {
    "findings": [],
    "issues": [],
    "score": 0
}
progress["scores"][check_name] = progress["partial_results"][check_name]["score"]
progress["last_updated"] = datetime.datetime.now().isoformat()

json.dump(progress, open(progress_file, "w"), ensure_ascii=False, indent=2)
print(f"✓ {check_name} ذخیره شد — امتیاز: {progress['scores'][check_name]}")
```

---

## گام ۵ — تولید گزارش‌ها

→ فرمت دقیق در `references/report-format.md`

```python
weights = {
    "observability": 20,
    "logging": 15,
    "security_network": 10,
    "security_database": 10,
    "security_app": 10,
    "arch": 10,
    "resilience": 10,
    "business_reporting": 5,
    "api_standards": 5,
    "cicd": 5,
}

# تنظیم وزن برای banking
if project_type == "banking":
    weights["observability"] += 3
    weights["resilience"] += 2
    weights["cicd"] -= 3
    weights["business_reporting"] -= 2

total = sum((progress["scores"].get(k, 0) / 100) * w for k, w in weights.items())
```

**راهنمای remediation-guide:**
- برای هر نقص، **کد نمونه واقعی** برای زبان پروژه بنویس
- اولویت: 🔴 Blocker → 🟠 مهم (Sprint بعدی) → 🟡 بهبود
- برای حوزه‌های `resilience` و `arch`، اگر پروژه `banking` است، همه نقص‌ها 🔴 هستند

---

## پیام در صورت کمبود Context

```
⚠️ Context در حال اتمام است.
Progress ذخیره شد: {output_dir}/audit-progress.json
Checks تکمیل‌شده: {completed_checks}
باقی‌مانده: {pending_checks}

برای ادامه در session جدید بگو:
"ادامه audit از {output_dir}"
```

---

## فایل‌های مرجع

- `references/checks.md` — دستورات bash و معیارهای هر check
- `references/report-format.md` — قالب دقیق فایل‌های خروجی
- `scripts/progress_manager.py` — ابزار مدیریت progress
