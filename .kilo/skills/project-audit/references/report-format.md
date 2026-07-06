# فرمت گزارش‌ها (v2.0)

## فایل ۱: audit-report.md

```markdown
# گزارش ممیزی پروژه — {project_name}

**تاریخ بررسی:** {date}
**نسخه:** {git_commit یا latest}
**بررسی‌کننده:** Project Audit Skill v2.0
**زبان/فریمورک:** {tech_stack}
**نوع پروژه:** {commercial / mvp / banking}

---

## خلاصه اجرایی

| معیار | امتیاز | وضعیت |
|-------|--------|--------|
| Observability & Tracing | X/20 | ✅/🟡/🔴 |
| Logging Standards | X/15 | ✅/🟡/🔴 |
| Network & Security | X/10 | ✅/🟡/🔴 |
| Database Security | X/10 | ✅/🟡/🔴 |
| Application Security | X/10 | ✅/🟡/🔴 |
| Architecture & Scalability | X/10 | ✅/🟡/🔴 |
| Resilience & DRP | X/10 | ✅/🟡/🔴 |
| Business Reporting | X/5 | ✅/🟡/🔴 |
| API Standards | X/5 | ✅/🟡/🔴 |
| CI/CD & Containerization | X/5 | ✅/🟡/🔴 |
| **مجموع** | **X/100** | **[سطح]** |

### وضعیت کلی: {✅ Production-Ready | 🟡 Near-Ready | 🟠 Needs Work | 🔴 Not Ready}

---

## مسدودکننده‌های حیاتی (Critical Blockers)

> این موارد باید **قبل از deploy** برطرف شوند — صرف‌نظر از امتیاز کلی.

- [ ] {مورد اول}
- [ ] {مورد دوم}

---

## جزئیات بررسی هر حوزه

### ۱. Observability & Tracing — {X}/20

| شناسه | بررسی | نتیجه | جزئیات |
|--------|-------|--------|---------|
| OBS-1 | OpenTelemetry نصب شده | ✅/❌ | {توضیح} |
| OBS-2 | Export به SigNoz | ✅/❌ | {توضیح} |
| OBS-3 | Trace ID propagation | ✅/❌ | {توضیح} |
| OBS-4 | Span تعریف‌شده | ✅/❌ | {توضیح} |
| OBS-5 | Health check با وابستگی‌ها | ✅/❌ | {توضیح} |
| OBS-6 | Alert rule خطاهای تکرارشونده | ✅/❌ | {توضیح} |
| OBS-7 | NTP sync | ✅/❌ | {توضیح} |
| OBS-8 | Gateway sample-rate | ✅/❌ | {توضیح} |

---

### ۲. Logging Standards — {X}/15

| شناسه | بررسی | نتیجه | جزئیات |
|--------|-------|--------|---------|
| LOG-1 | Structured logging | ✅/❌ | {توضیح} |
| LOG-2 | requestId در لاگ | ✅/❌ | {توضیح} |
| LOG-3 | Log levels صحیح | ✅/❌ | {توضیح} |
| LOG-4 | Sensitive data mask شده | ✅/❌ | {توضیح} |
| LOG-5 | Error catalog موجود | ✅/❌ | {توضیح} |

---

### ۳. Network & Security — {X}/10

| شناسه | بررسی | نتیجه | جزئیات |
|--------|-------|--------|---------|
| SEC-N1 | HTTPS/TLS | ✅/❌ | {توضیح} |
| SEC-N2 | Rate limiting | ✅/❌ | {توضیح} |
| SEC-N3 | CORS configuration | ✅/❌ | {توضیح} |
| SEC-N4 | No hardcoded secrets | ✅/❌ | {توضیح} |
| SEC-N5 | Circuit breaker خارجی | ✅/❌ | {توضیح} |

---

### ۴. Database Security — {X}/10

| شناسه | بررسی | نتیجه | جزئیات |
|--------|-------|--------|---------|
| DB-1 | Parameterized queries | ✅/❌ | {توضیح} |
| DB-2 | Connection string در env | ✅/❌ | {توضیح} |
| DB-3 | Backup strategy | ✅/❌ | {توضیح} |
| DB-4 | Replication پیکربندی | ✅/❌ | {توضیح} |
| DB-5 | ایندکس‌گذاری مستند | ✅/❌ | {توضیح} |

---

### ۵. Application Security — {X}/10

| شناسه | بررسی | نتیجه | جزئیات |
|--------|-------|--------|---------|
| APP-1 | Authentication امن | ✅/❌ | {توضیح} |
| APP-2 | Password hashing | ✅/❌ | {توضیح} |
| APP-3 | Input validation | ✅/❌ | {توضیح} |
| APP-4 | Audit trail ادمین‌ها | ✅/❌ | {توضیح} |
| APP-5 | Dependency scanning | ✅/❌ | {توضیح} |

---

### ۶. Architecture & Scalability — {X}/10 ← جدید

| شناسه | بررسی | نتیجه | جزئیات |
|--------|-------|--------|---------|
| ARCH-1 | ساختار ماژولار | ✅/❌ | {توضیح} |
| ARCH-2 | Dependency Injection | ✅/❌ | {توضیح} |
| ARCH-3 | Abstraction layer برای فناوری | ✅/❌ | {توضیح} |
| ARCH-4 | Stateless / مقیاس‌پذیری افقی | ✅/❌ | {توضیح} |
| ARCH-5 | مستند معماری | ✅/❌ | {توضیح} |

---

### ۷. Resilience & DRP — {X}/10 ← جدید

| شناسه | بررسی | نتیجه | جزئیات |
|--------|-------|--------|---------|
| RES-1 | تست فشار + نتایج مستند | ✅/❌ | {توضیح} |
| RES-2 | DRP / RTO/RPO مستند | ✅/❌ | {توضیح} |
| RES-3 | Graceful shutdown | ✅/❌ | {توضیح} |
| RES-4 | سناریوی قطع سرویس خارجی | ✅/❌ | {توضیح} |
| RES-5 | Memory leak بررسی شده | ✅/❌ | {توضیح} |

---

### ۸. Business Reporting — {X}/5

| شناسه | بررسی | نتیجه | جزئیات |
|--------|-------|--------|---------|
| BIZ-1 | Queue-based events | ✅/❌ | {توضیح} |
| BIZ-2 | Event schema | ✅/❌ | {توضیح} |

---

### ۹. API Standards — {X}/5

| شناسه | بررسی | نتیجه | جزئیات |
|--------|-------|--------|---------|
| API-1 | OpenAPI spec | ✅/❌ | {توضیح} |
| API-2 | Semantic versioning | ✅/❌ | {توضیح} |
| API-3 | Breaking change policy | ✅/❌ | {توضیح} |

---

### ۱۰. CI/CD & Containerization — {X}/5 ← جدید

| شناسه | بررسی | نتیجه | جزئیات |
|--------|-------|--------|---------|
| CICD-1 | Dockerfile موجود | ✅/❌ | {توضیح} |
| CICD-2 | CI pipeline | ✅/❌ | {توضیح} |
| CICD-3 | مات standard | ✅/❌ | {توضیح} |

---

*گزارش توسط Project Audit Skill v2.0 تولید شده — بر اساس استانداردهای داخلی شرکت*
```

---

## فایل ۲: remediation-guide.md

```markdown
# راهنمای رفع نقص‌ها — {project_name}

**تاریخ:** {date}
**بر اساس گزارش:** audit-report.md

---

## اولویت‌بندی کارها

### 🔴 فوری (قبل از deploy — Blockers)

#### {شناسه}: {عنوان نقص}

**مشکل:** {توضیح دقیق}

**راه‌حل برای {tech_stack}:**

```bash
pip install {package}
```

```python
# مثال کد پیاده‌سازی
{کد نمونه دقیق برای زبان پروژه}
```

**فایل‌هایی که باید تغییر کنند:**
- `{path/to/file.py}` — {توضیح تغییر}

**تخمین زمان:** {X ساعت/روز}

---

### 🟠 مهم (در Sprint بعدی)

{همان ساختار بالا}

---

### 🟡 بهبود (بلندمدت)

{همان ساختار بالا}

---

## چک‌لیست تکمیل

- [ ] 🔴 {نقص اول}
- [ ] 🔴 {نقص دوم}
- [ ] 🟠 {نقص سوم}
- [ ] 🟡 {نقص چهارم}

---

## منابع مفید

- [OpenTelemetry Python](https://opentelemetry.io/docs/instrumentation/python/)
- [OpenTelemetry Node.js](https://opentelemetry.io/docs/instrumentation/js/)
- [SigNoz Setup](https://signoz.io/docs/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [12 Factor App](https://12factor.net/)
- [Circuit Breaker Pattern](https://martinfowler.com/bliki/CircuitBreaker.html)

*راهنما بر اساس استانداردهای داخلی شرکت تولید شده — v2.0*
```
