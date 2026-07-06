# Checks Reference — جزئیات هر بررسی (v2.0)

## فهرست مطالب
1. [OBS] Observability & Tracing
2. [LOG] Logging Standards
3. [SEC-NET] Network & Security
4. [SEC-DB] Database Security
5. [SEC-APP] Application Security
6. [ARCH] Architecture & Scalability ← **جدید**
7. [RESILIENCE] Resilience & DRP ← **جدید**
8. [BIZ] Business Reporting Pipeline
9. [API] API Standards
10. [CICD] CI/CD & Containerization ← **جدید**

---

## [OBS] Observability & Tracing

**وزن:** 20 امتیاز از ۱۰۰

### الزامات اجباری (هر کدام ۳ امتیاز — جمع ۱۸)

| # | بررسی | نحوه تشخیص |
|---|-------|------------|
| OBS-1 | OpenTelemetry نصب و پیکربندی شده | `opentelemetry` در requirements/package.json، import در کد |
| OBS-2 | داده به SigNoz ارسال می‌شود | config فایل‌ها، env vars با `OTEL_EXPORTER_*` |
| OBS-3 | Trace ID در تمام سرویس‌ها propagate می‌شود | جستجوی `trace_id`, `traceId`, `X-Trace-Id` در کد |
| OBS-4 | Span برای هر service call تعریف شده | جستجوی `tracer.start_span`, `with tracer.start_as_current_span` |
| OBS-5 | Health check endpoint با بررسی وابستگی‌ها | `/health` یا `/readiness` که DB، cache و سرویس‌های خارجی را چک کند |
| OBS-6 | Alert rule برای خطاهای تکرارشونده | rule در SigNoz/Grafana برای error rate یا pattern خطا |

### الزامات تکمیلی (جمع ۲ امتیاز)

| # | بررسی | نحوه تشخیص |
|---|-------|------------|
| OBS-7 | NTP sync ماشین‌ها | بررسی مستندات ops یا chronyc/timedatectl در Dockerfile |
| OBS-8 | Gateway sample-rate config | OTEL config با `OTEL_TRACES_SAMPLER_ARG` یا sampler در gateway |

### نحوه بررسی
```bash
# Python
grep -r "opentelemetry\|otel\|tracer\|trace_id" {repo_path} \
  --include="*.py" -l

# Node.js
grep -r "@opentelemetry\|tracer\|traceId" {repo_path} \
  --include="*.js" --include="*.ts" -l

# health check
grep -rn "health\|readiness\|liveness" {repo_path} \
  --include="*.py" --include="*.js" --include="*.ts" | grep -i "route\|endpoint\|path"

# alert rule
grep -r "alert\|AlertRule\|threshold" {repo_path} \
  --include="*.yml" --include="*.yaml" -l

# NTP
grep -r "ntp\|chrony\|timesyncd" {repo_path} \
  --include="Dockerfile*" --include="*.yml"
```

---

## [LOG] Logging Standards

**وزن:** 15 امتیاز از ۱۰۰

### الزامات (هر کدام ۳ امتیاز)

| # | بررسی | نحوه تشخیص |
|---|-------|------------|
| LOG-1 | Structured logging (JSON) استفاده می‌شود | کتابخانه‌های structlog, winston, zerolog، یا JSON formatter |
| LOG-2 | هر لاگ حاوی requestId/traceId است | جستجوی `request_id`, `trace_id` در log statements |
| LOG-3 | Log levels صحیح استفاده می‌شود (DEBUG/INFO/WARNING/ERROR/CRITICAL) | بررسی استفاده از سطوح مختلف |
| LOG-4 | اطلاعات حساس (password, token, card) mask شده | جستجوی الگوی mask/redact |
| LOG-5 | Error catalog و راهنمای خطایابی وجود دارد | فایل `error-catalog.md` یا مستندات مشابه با کد خطا + مسیر بررسی |

### نحوه بررسی
```bash
# structured logging
grep -r "structlog\|json.*format\|JsonFormatter\|winston\|zerolog" \
  {repo_path} --include="*.py" --include="*.js" --include="*.ts" -l

# sensitive data در لاگ (خطرناک)
grep -rn "log.*password\|log.*token\|log.*secret\|log.*card_number" \
  {repo_path} --include="*.py" --include="*.js"

# error catalog
find {repo_path} -name "error-catalog*" -o -name "errors.md" \
  -o -name "troubleshooting*" 2>/dev/null

# request_id
grep -rn "request_id\|requestId\|req_id\|correlation_id" \
  {repo_path} --include="*.py" --include="*.js" --include="*.ts"
```

---

## [SEC-NET] Network & Security

**وزن:** 10 امتیاز از ۱۰۰

### الزامات (هر کدام ۲ امتیاز)

| # | بررسی | نحوه تشخیص |
|---|-------|------------|
| SEC-N1 | HTTPS/TLS برای ارتباطات خارجی | ssl_context, TLS config در کد |
| SEC-N2 | Rate limiting (در gateway یا service) | middleware‌های rate limit، nginx config |
| SEC-N3 | CORS صحیح پیکربندی شده | CORS settings، allowed origins |
| SEC-N4 | Secrets در environment variables (نه hardcode) | جستجوی strings مشکوک در کد |
| SEC-N5 | Circuit breaker برای سرویس‌های خارجی | `circuit_breaker`, `retry`, `timeout` در کد |

### نحوه بررسی
```bash
# hardcoded secrets
grep -rn "api_key\s*=\s*['\"][^'\"$]" {repo_path} \
  --include="*.py" --include="*.js" --include="*.ts"
grep -rn "password\s*=\s*['\"][^'\"$]" {repo_path}

# rate limiting
grep -r "RateLimiter\|rate_limit\|throttle\|slowDown" {repo_path} \
  --include="*.py" --include="*.js" -l

# circuit breaker
grep -r "circuit.breaker\|CircuitBreaker\|resilience4j\|pybreaker\|opossum" \
  {repo_path} -l
```

---

## [SEC-DB] Database Security

**وزن:** 10 امتیاز از ۱۰۰

### الزامات (هر کدام ۲ امتیاز)

| # | بررسی | نحوه تشخیص |
|---|-------|------------|
| DB-1 | Parameterized queries / ORM (جلوگیری از SQL Injection) | ORM استفاده می‌شود |
| DB-2 | Connection string در env var (نه hardcode) | DATABASE_URL در env |
| DB-3 | Backup strategy مستند شده | script پشتیبان‌گیری، مستندات |
| DB-4 | Replication پیکربندی شده | replica config، read/write separation |
| DB-5 | ایندکس‌گذاری با مشورت تیم DB مستند شده | migration files با INDEX، یا مستندات DB design |

### نحوه بررسی
```bash
# SQL injection risk (raw queries)
grep -rn "f\"SELECT\|f'SELECT\|format.*SELECT\|%.*SELECT" \
  {repo_path} --include="*.py"

# ORM usage
grep -r "SQLAlchemy\|Prisma\|TypeORM\|Django ORM\|GORM" \
  {repo_path} -l

# replication / read replica
grep -r "replica\|read_replica\|slave\|REPLICA\|READ_HOST" \
  {repo_path} --include="*.py" --include="*.js" --include="*.env*" --include="*.yml"

# index در migrations
grep -r "CREATE INDEX\|createIndex\|add_index" \
  {repo_path} -l
```

---

## [SEC-APP] Application Security

**وزن:** 10 امتیاز از ۱۰۰

### الزامات (هر کدام ۲ امتیاز)

| # | بررسی | نحوه تشخیص |
|---|-------|------------|
| APP-1 | Authentication با JWT یا session امن | استفاده از کتابخانه‌های معتبر |
| APP-2 | Password hashing امن (bcrypt, argon2) | جستجوی hash function |
| APP-3 | Input validation در همه endpoints | validator middleware، Pydantic، Joi |
| APP-4 | Audit trail برای اپراتورها و ادمین‌ها | لاگ عملیات admin، audit log جدا |
| APP-5 | Dependency vulnerability scan موجود | dependabot، snyk، safety |

### نحوه بررسی
```bash
# password hashing
grep -r "bcrypt\|argon2\|passlib\|hashlib" {repo_path} -l
# خطرناک:
grep -rn "md5.*password\|sha1.*password" {repo_path}

# audit log
grep -r "audit\|audit_log\|AuditLog\|admin.*log" \
  {repo_path} --include="*.py" --include="*.js" -l

# input validation
grep -r "pydantic\|joi\|yup\|class-validator\|marshmallow" \
  {repo_path} -l

# security scan config
grep -r "snyk\|dependabot\|safety\|bandit\|semgrep" \
  {repo_path} --include="*.yml" --include="*.yaml"
```

---

## [ARCH] Architecture & Scalability ← جدید

**وزن:** 10 امتیاز از ۱۰۰

### الزامات (هر کدام ۲ امتیاز)

| # | بررسی | نحوه تشخیص |
|---|-------|------------|
| ARCH-1 | ساختار ماژولار: business logic از framework/DB جدا است | پوشه‌بندی با لایه‌های مجزا، abstraction layer |
| ARCH-2 | Dependency Injection پیاده‌سازی شده | DI container، constructor injection |
| ARCH-3 | معماری از مهاجرت فناوری پشتیبانی می‌کند | interface/abstract class برای DB/cache/queue |
| ARCH-4 | مقیاس‌پذیری افقی پشتیبانی می‌شود (stateless) | عدم state محلی، استفاده از shared cache |
| ARCH-5 | مستند معماری موجود است | فایل `ARCHITECTURE.md` یا ADR ها |

### نحوه بررسی
```bash
# ساختار پوشه‌ها
find {repo_path}/src {repo_path}/app {repo_path}/lib -maxdepth 2 \
  -type d 2>/dev/null | grep -v node_modules | grep -v __pycache__

# abstraction / interface
grep -r "abstract class\|Interface\|Protocol\|ABC\|@injectable" \
  {repo_path} --include="*.py" --include="*.ts" -l

# stateless (بدون session محلی)
grep -rn "global\s\+[A-Z]\|module.state\|singleton" \
  {repo_path} --include="*.py" --include="*.js" | grep -v test | head -20

# مستند معماری
find {repo_path} -name "ARCHITECTURE*" -o -name "ADR*" \
  -o -name "design*.md" -o -name "architecture*.md" 2>/dev/null

# DI
grep -r "inject\|Injectable\|@Inject\|container.bind\|provide.*inject" \
  {repo_path} --include="*.py" --include="*.ts" -l
```

---

## [RESILIENCE] Resilience & DRP ← جدید

**وزن:** 10 امتیاز از ۱۰۰

### الزامات (هر کدام ۲ امتیاز)

| # | بررسی | نحوه تشخیص |
|---|-------|------------|
| RES-1 | تست فشار (load test) انجام شده و نتایج مستند است | فایل‌های k6/locust/jmeter، یا گزارش تست فشار |
| RES-2 | DRP (Disaster Recovery Plan) یا RTO/RPO مستند است | مستندات `drp.md` یا بخش disaster recovery |
| RES-3 | Graceful shutdown پیاده‌سازی شده | handler برای SIGTERM، drain connections |
| RES-4 | سناریوی قطع سرویس خارجی مستند است | مستند "اگر X قطع شد چه می‌شود" + fallback |
| RES-5 | Memory leak بررسی شده (یا test دارد) | profiling در CI، یا load test با بررسی memory |

### نحوه بررسی
```bash
# load test files
find {repo_path} -name "*.k6.js" -o -name "locustfile.py" \
  -o -name "*.jmx" -o -name "*load*test*" 2>/dev/null

# DRP documentation
find {repo_path} -iname "drp*" -o -iname "disaster*" \
  -o -iname "recovery*" -o -iname "runbook*" 2>/dev/null

# graceful shutdown
grep -rn "SIGTERM\|graceful\|shutdown\|drain\|beforeExit" \
  {repo_path} --include="*.py" --include="*.js" --include="*.ts"

# fallback / circuit breaker
grep -r "fallback\|circuit.breaker\|retry.*max\|timeout.*config" \
  {repo_path} --include="*.py" --include="*.js" -l
```

---

## [BIZ] Business Reporting Pipeline

**وزن:** 5 امتیاز از ۱۰۰

### الزامات (هر کدام ۲.۵ امتیاز)

| # | بررسی | نحوه تشخیص |
|---|-------|------------|
| BIZ-1 | Business events به queue (نه مستقیم به log) ارسال می‌شود | Kafka, RabbitMQ, Redis Queue در کد |
| BIZ-2 | Event schema مستند شده | مستندات event، schema definition |

### نحوه بررسی
```bash
grep -r "kafka\|rabbitmq\|celery\|redis.*queue\|bull\|bullmq" \
  {repo_path} -l --include="*.py" --include="*.js"
```

---

## [API] API Standards

**وزن:** 5 امتیاز از ۱۰۰

### الزامات (هر کدام ~1.7 امتیاز)

| # | بررسی | نحوه تشخیص |
|---|-------|------------|
| API-1 | OpenAPI/Swagger spec وجود دارد | swagger.json, openapi.yaml |
| API-2 | Semantic versioning در API (مثلاً /v1/) | versioned URLs |
| API-3 | Breaking change policy مستند است | CHANGELOG یا migration guide با تعریف breaking changes |

### نحوه بررسی
```bash
# OpenAPI
find {repo_path} -name "swagger*" -o -name "openapi*" 2>/dev/null

# versioned endpoints
grep -rn "\/v[0-9]\/" {repo_path} \
  --include="*.py" --include="*.js" --include="*.ts" | head -10

# changelog / breaking changes
find {repo_path} -iname "CHANGELOG*" -o -iname "MIGRATION*" 2>/dev/null
grep -r "breaking.change\|BREAKING" {repo_path} \
  --include="*.md" -l 2>/dev/null
```

---

## [CICD] CI/CD & Containerization ← جدید

**وزن:** 5 امتیاز از ۱۰۰

### الزامات (هر کدام ~1.7 امتیاز)

| # | بررسی | نحوه تشخیص |
|---|-------|------------|
| CICD-1 | Dockerfile و docker-compose موجود است | `Dockerfile`, `docker-compose.yml` |
| CICD-2 | CI pipeline برای test و build وجود دارد | `.github/workflows/`, `.gitlab-ci.yml` |
| CICD-3 | استانداردهای مات (MAAT) رعایت شده | package.json scripts، مطابق با مستندات مات |

### نحوه بررسی
```bash
# containerization
find {repo_path} -name "Dockerfile*" -o -name "docker-compose*" 2>/dev/null

# CI pipeline
find {repo_path} -name ".gitlab-ci.yml" \
  -o -path "*/.github/workflows/*.yml" 2>/dev/null

# مات standard (بررسی scripts)
cat {repo_path}/package.json 2>/dev/null | python3 -c \
  "import json,sys; d=json.load(sys.stdin); print(d.get('scripts', {}))"
```

---

## امتیازدهی نهایی

| امتیاز | سطح | توضیح |
|--------|------|-------|
| ۹۰-۱۰۰ | ✅ Production-Ready | آماده deploy |
| ۷۵-۸۹ | 🟡 Near-Ready | چند نقص قابل رفع |
| ۶۰-۷۴ | 🟠 Needs Work | نیاز به بهبود جدی |
| زیر ۶۰ | 🔴 Not Ready | مسدودکننده‌های جدی وجود دارد |

### Blocker های مطلق (صرف‌نظر از امتیاز کلی)

موارد زیر به‌تنهایی مانع انتشار هستند — حتی اگر امتیاز کلی بالا باشد:
- OBS-3 نقص دارد (Trace ID propagate نمی‌شود)
- LOG-4 نقص دارد (داده حساس در لاگ)
- SEC-N4 نقص دارد (secret hardcode شده)
- DB-1 نقص دارد (SQL injection risk)
- APP-2 نقص دارد (password بدون hashing)
