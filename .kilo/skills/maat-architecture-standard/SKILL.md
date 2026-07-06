---
name: maat-architecture-standard
description: >
  Canonical reference for the Maat Architecture Standard — the organisation's
  unified 6-layer infrastructure pattern for deploying services. Defines the
  mandatory rules for Hard Gateway Entry, VLAN Isolation, Least Privilege Access,
  Layer Separation, Base Service Access, and Egress Gateway patterns.
  Use this skill whenever you need to verify compliance against the Maat
  standard, understand the layer model, or reference the mandatory architecture
  rules for deployment.
---

# Maat Architecture Standard
# استاندارد معماری مات

> **Version:** 1.0  
> **Audience:** Architects, Backend Engineers, DevOps, AI Agents  
> **Status:** Active Standard  
> **Language:** Bilingual (FA / EN)

---

## 1. Purpose / هدف

**EN:**  
This document defines the **Maat Architecture Standard** — the organization's unified infrastructure pattern for deploying services. It applies to all new projects that use internal company tooling. The architecture is not named after a specific framework; it is a synthesis of standard patterns (layered isolation, gateway-enforced access, VLAN segmentation) formalized as an organizational requirement.

**FA:**  
این سند، **استاندارد معماری مات** را تعریف می‌کند — الگوی یکپارچه زیرساخت سازمان برای استقرار سرویس‌ها. این استاندارد برای تمام پروژه‌های جدیدی که از ابزارهای داخلی شرکت استفاده می‌کنند اعمال می‌شود. این معماری وابسته به فریم‌ورک خاصی نیست؛ بلکه ترکیبی از الگوهای رایج (ایزوله‌سازی لایه‌ای، کنترل دسترسی از طریق Gateway، تفکیک VLAN) است که به عنوان الزام سازمانی رسمی شده است.

---

## 2. Core Principles / اصول بنیادین

| # | Principle | اصل |
|---|-----------|-----|
| 1 | **Hard Gateway Entry** | هیچ درخواست خارجی بدون عبور از Gateway مجاز به ورود نیست |
| 2 | **VLAN Isolation** | هر لایه در یک VLAN ایزوله مستقر می‌شود؛ دسترسی پیش‌فرض وجود ندارد |
| 3 | **Least Privilege Access** | دسترسی‌ها باید دقیقاً در سطح container-to-container و port-to-port تعریف شوند، نه machine-to-machine |
| 4 | **Layer Separation** | هر لایه مسئولیت مشخص دارد و در محیط جداگانه‌ای مستقر می‌شود |
| 5 | **Tooling Agnosticism** | ابزارهای پیاده‌سازی قابل تعویض هستند؛ **مفهوم لایه باید حفظ شود** |
| 6 | **Universal Base Service Access** | تمام سرویس‌ها باید به Base Services (Logging, Monitoring) دسترسی داشته باشند |
| 7 | **External Output via Dedicated Gateway** | تمام خروجی به سرویس‌های خارجی باید از طریق Gateway اختصاصی انجام شود |

---

## 3. Architecture Layers / لایه‌های معماری

معماری مات از **۶ لایه** تشکیل شده است. هر لایه به صورت مستقل مستقر می‌شود و در محیط ایزوله خود قرار دارد.

> ⚠️ **مهم / Important:** نام‌های ابزار در هر لایه **مثال** هستند. مفهوم لایه ثابت است، ابزار قابل تعویض است.  
> Tool names in each layer are **examples**. The layer concept is fixed; the tooling is replaceable.

---

### Layer 1 — Core

**EN:** Foundational services that all other layers depend on.  
**FA:** سرویس‌های پایه‌ای که تمام لایه‌های دیگر به آن‌ها وابسته هستند.

| Responsibility | Example Tooling | Replaceable |
|----------------|-----------------|-------------|
| Internal DNS | dns-recursor, dns-authoritative | ✅ Any DNS resolver |
| Centralized Logging | OpenSearch, Fluentd | ✅ Any log aggregator |
| Monitoring & Metrics | Prometheus, Grafana | ✅ Any monitoring stack |
| Secrets Management | Vault | ✅ Any secrets manager |
| Core Database | PostgreSQL (core-pg) | ✅ |

**Rules / قوانین:**
- All services in all other layers **MUST** connect to the Logging and Monitoring services of this layer.
- تمام سرویس‌های سایر لایه‌ها **باید** به Logging و Monitoring این لایه متصل باشند.
- This layer may be **shared** across services in the same environment.
- این لایه ممکن است به صورت **اشتراکی** بین سرویسهای این محیط استفاده شود.

---

### Layer 2 — Database

**EN:** All persistent data storage for the project.  
**FA:** تمام ذخیره‌سازی داده‌های پایدار پروژه.

| Responsibility | Example Tooling | Replaceable |
|----------------|-----------------|-------------|
| Primary Datastore | Atlas 4, PostgreSQL | ✅ Any RDBMS/NoSQL |

**Rules / قوانین:**
- Only explicitly permitted services may access this layer.
- فقط سرویس‌هایی که **صریحاً مجاز شده‌اند** می‌توانند به این لایه دسترسی داشته باشند.
- Access must be defined at **container + port** level, not VLAN-wide.
- دسترسی باید در سطح **container + port** تعریف شود، نه در سطح VLAN کلی.

---

### Layer 3 — Public Services

**EN:** Shared organizational services used by multiple projects.  
**FA:** سرویس‌های مشترک سازمانی که توسط چندین پروژه استفاده می‌شوند.

| Responsibility | Example Tooling | Replaceable |
|----------------|-----------------|-------------|
| Authentication | authentication service | ✅ Any IdP/Auth service |
| Authorization | authorization service | ✅ |
| Identity & Access Management | Samad | ✅ Any IAM service |
| User Management | usermanager | ✅ |
| OTP | otp service | ✅ |
| Config Management | configManagement / CCS | ✅ Any config server |
| Scheduled Tasks | cron service | ✅ |
| Payment Adapter | payment | ✅ |
| Captcha | captcha | ✅ |
| Shared Cache | Redis (public) | ✅ Any shared cache |

**Rules / قوانین:**
- This layer is **shared** across all projects in an environment.
- این لایه **اشتراکی** است و برای تمام پروژه‌ها مشترک است.
- New projects **must not** re-implement services that already exist in this layer.
- پروژه‌های جدید **نباید** سرویس‌های موجود در این لایه را دوباره پیاده‌سازی کنند.

---

### Layer 4 — Gateway

**EN:** The sole authorized entry point for all external requests.  
**FA:** تنها نقطه ورود مجاز برای تمام درخواست‌های خارجی.

| Responsibility | Example Tooling | Replaceable |
|----------------|-----------------|-------------|
| Request Entry Point | API Gateway | ✅ Any API gateway |
| Authentication Enforcement | Enforced at gateway | — |
| Authorization Enforcement | Enforced at gateway | — |

**Rules / قوانین:**
- **No** external request may bypass this layer — no exceptions.
- **هیچ** درخواست خارجی بدون عبور از این لایه مجاز نیست — بدون استثنا.
- The Gateway authenticates and authorizes once at entry; internal services do not re-authenticate.
- Gateway یک‌بار در ورودی احراز هویت می‌کند؛ سرویس‌های داخلی نیازی به re-authentication ندارند.
- Gateway has access to Project Services; it does **not** have direct access to the Database layer by default.

---

### Layer 5 — File Storage

**EN:** Isolated storage for large files and binary assets.  
**FA:** ذخیره‌سازی ایزوله برای فایل‌های حجیم و binary assets.

| Responsibility | Example Tooling | Replaceable |
|----------------|-----------------|-------------|
| File/Object Storage | filestorage service | ✅ MinIO, S3, Ceph, any object store |

**Rules / قوانین:**
- This layer **must** be isolated from the main transaction flow to prevent resource contention.
- این لایه باید از جریان اصلی تراکنش‌ها **ایزوله** باشد تا رشد حجم فایل‌ها بر سایر لایه‌ها تأثیر نگذارد.
- The Gateway may directly route to this layer when needed.

---

### Layer 6 — Project Services

**EN:** The core business logic of the project. This is the only layer whose size varies per project.  
**FA:** منطق اصلی کسب‌وکار پروژه. تنها لایه‌ای که ابعاد آن از پیش مشخص نیست و بر اساس پروژه تعریف می‌شود.

**Rules / قوانین:**
- Each service must **explicitly declare** which services it needs to communicate with (including layer and port).
- هر سرویس باید **صریحاً** مشخص کند به کدام سرویس‌ها (در هر لایه) نیاز دارد.
- All services in this layer must connect to Base Services (Layer 1).
- Services reside in an isolated VLAN; no implicit access to any other service exists.
- سرویس‌ها در VLAN ایزوله هستند؛ هیچ دسترسی ضمنی به سرویس دیگری وجود ندارد.

---

## 4. Deployment Modes / حالت‌های استقرار

معماری مات در **دو حالت** قابل استقرار است. قوانین بنیادین در **هر دو حالت** اجباری هستند.

---

### Mode A — Containerized (e.g., Kondo / Simurgh)

**EN:** Services run as containers managed by an internal container orchestration system.  
**FA:** سرویس‌ها به صورت container در سیستم orchestration داخلی اجرا می‌شوند.

| Feature | Detail |
|---------|--------|
| Deployment unit | Container |
| Isolation | VLAN per VM group, managed via orchestration UI |
| Access management | Container-to-container access on specific port, configured via UI |
| Internal Proxy | One proxy per VM, routing requests between containers on that VM |

**Key advantage:** Fine-grained access control (container + port) is manageable via UI without manual network configuration.

---

### Mode B — Non-Containerized (VM-based)

**EN:** Each service runs on a dedicated Virtual Machine.  
**FA:** هر سرویس روی یک ماشین مجازی مجزا اجرا می‌شود.

| Feature | Detail |
|---------|--------|
| Deployment unit | Virtual Machine |
| Isolation | VLAN per VM, managed by network/infrastructure team |
| Access management | Via network configuration by infrastructure team |
| DNS | Internal company DNS (managed by network team) |
| Base Services | May be shared across projects in the same environment |
| Internal Proxy | Optional — recommended if rollout management is needed |

**Note / نکته:** در این حالت سرویس‌های هم‌VLAN به صورت پیش‌فرض به یکدیگر دسترسی دارند؛ بنابراین تعریف دسترسی‌ها باید با دقت بیشتری انجام شود.  
In this mode, services within the same VLAN can reach each other by default; access definition requires extra care.

---

## 5. Mandatory Rules / قوانین الزامی

این قوانین در **هر دو Deployment Mode** و برای **تمام پروژه‌ها** اجباری هستند.

---

### Rule 1 — Hard Gateway Entry

```
ALL external client requests MUST pass through the Gateway layer.
Authentication and Authorization MUST be enforced at the Gateway.
No exceptions.
```
تمام درخواست‌های خارجی باید از Gateway عبور کنند. احراز هویت و تعیین سطح دسترسی در Gateway اجرا می‌شود. بدون استثنا.

---

### Rule 2 — VLAN Isolation

```
Each deployment unit (VM or Container group) MUST reside in an isolated VLAN.
Default inter-VLAN access is DENIED.
All cross-VLAN access must be explicitly granted and documented.
```
هر واحد استقرار در VLAN ایزوله قرار می‌گیرد. دسترسی بین VLAN‌ها به صورت پیش‌فرض ممنوع است. تمام دسترسی‌های cross-VLAN باید صریحاً مجاز شوند و مستند شوند.

---

### Rule 3 — Least Privilege Access

```
Access rules MUST be defined at container-to-container + port level.
Machine-to-machine blanket access is FORBIDDEN.

Correct:   authentication container → database container : port 5432
Incorrect: services VM             → database VM         (entire machine)
```
دسترسی‌ها باید در سطح container+port تعریف شوند. دسترسی کلی machine-to-machine ممنوع است.

---

### Rule 4 — Mandatory Base Service Access

```
ALL services, in ALL layers, MUST have access to:
  - Centralized Logging  (e.g., log aggregator + search)
  - Monitoring & Metrics (e.g., metrics collector)

This is the ONLY default-open access in the architecture.
```
تمام سرویس‌ها باید به Logging و Monitoring متصل باشند. این تنها دسترسی پیش‌فرض باز در معماری است.

---

### Rule 5 — Layer Separation

```
Each layer MUST be deployed in isolation:
  Core | Database | Public Services | Gateway | File Storage | Project Services

Merging layers into a single deployment unit is FORBIDDEN
unless explicitly approved by the Architecture team.
```
هر لایه باید به صورت مجزا مستقر شود. ادغام لایه‌ها ممنوع است مگر با تأیید صریح تیم معماری.

---

### Rule 6 — No Re-authentication on Internal Traffic

```
After a request passes the Gateway (authenticated + authorized),
internal service-to-service calls do NOT require re-authentication
through the Gateway.
Direct internal calls are permitted within the defined access rules.
```
پس از احراز هویت اولیه در Gateway، ارتباطات داخلی نیازی به عبور مجدد از Gateway ندارند.

---

### Rule 7 — External Output via Dedicated Egress Gateway

```
ALL outbound calls to external systems MUST go through
a dedicated Egress Gateway for that specific external system.
Direct outbound calls that bypass the Egress Gateway are FORBIDDEN.
```
تمام خروجی‌ها به سیستم‌های خارجی باید از طریق Egress Gateway اختصاصی آن سیستم انجام شوند.

---

### Rule 8 — Cross-Project Communication via Gateway

```
When Project A communicates with Project B (another internal project),
the request MUST be sent to Project B's Gateway — not directly to
Project B's internal services.
Project B's Gateway handles authentication and authorization before forwarding.
```
ارتباط با پروژه‌های داخلی دیگر باید از طریق Gateway آن پروژه انجام شود، نه مستقیم به سرویس‌های داخلی آن.

---

## 6. Traffic Flow / جریان درخواست‌ها

### Inbound Request Flow (External → System)

```
[Client / User]
      │
      ▼
┌─────────────────────────────────────────┐
│  LAYER 4 — GATEWAY                      │
│  ► Authentication enforced              │
│  ► Authorization enforced               │
└──────┬──────────────────────────────────┘
       │
       ├──────────────────────────────────────► [Layer 5: File Storage]
       │
       ▼
┌─────────────────────────────────────────┐
│  LAYER 6 — PROJECT SERVICES             │
│  (Business logic, after auth at gateway)│
└──────┬──────────────────────────────────┘
       │  (explicit access only, per access map)
       ├──► [Layer 2: Database]
       ├──► [Layer 3: Public Services]  (auth, IAM, config, cache...)
       └──► [Layer 5: File Storage]

ALL LAYERS ──► [Layer 1: Core]  (Logging + Monitoring — always open)
```

### Outbound Request Flow (System → External)

```
[Layer 6: Project Services]
      │
      ▼
[Egress Gateway — dedicated per external system]
      │
      ▼
[External System]
```

### Cross-Project Request Flow

```
[Project A — Layer 6 Services]
      │
      ▼
[Project B — Layer 4 Gateway]   ◄── Auth/Authz re-enforced at Project B boundary
      │
      ▼
[Project B — Layer 6 Services]
```

---

## 7. Internal Proxy (Selective) / پروکسی داخلی (انتخابی)

**EN:** Use of an internal proxy in front of each service is **optional** but recommended when rollout management or enhanced internal security is needed.  
**FA:** استفاده از پروکسی داخلی در جلوی هر سرویس **اجباری نیست** اما در پروژه‌هایی که به rollout management یا امنیت داخلی بیشتری نیاز دارند توصیه می‌شود.

### When to Use / چه زمانی استفاده شود

| Scenario | Proxy Recommended |
|----------|------------------|
| Canary / Blue-Green rollout needed | ✅ Yes |
| Internal rate limiting needed | ✅ Yes |
| Simple service, no complex rollout | ⚪ Optional |
| Containerized mode (per-VM) | ✅ One proxy per VM |

### Proxy Pattern / الگوی پروکسی

**Without Proxy:**
```
[Caller / Gateway] ──► [Service: port 80]
```

**With Proxy:**
```
[Caller / Gateway] ──► [Proxy: port 80] ──► [Service: port 8000]
                              │
                              └── manages: routing, rollout, internal security
```

> **Tooling Note:** The proxy tool (Nginx, Envoy, Traefik, or any reverse proxy) is **replaceable**.  
> The concept: one proxy sits between the caller and the service, owning routing and rollout decisions.

---

## 8. External Communication / ارتباطات برون‌سازمانی

### Egress Gateway Pattern

هر سیستم خارجی که پروژه با آن ارتباط دارد باید یک **Egress Gateway اختصاصی** داشته باشد.  
Each external system the project communicates with must have a **dedicated Egress Gateway**.

```
[Project Services]
      ├──► [Egress Gateway: External System A] ──► External System A
      └──► [Egress Gateway: External System B] ──► External System B
```

**Why / چرا:**
- Centralized outbound authentication and logging.
- Internal services remain isolated from external system details.
- سرویس‌های داخلی از جزئیات ارتباط خارجی ایزوله می‌مانند و logging خروجی در نقطه متمرکز انجام می‌شود.

---

## 9. Architecture Diagram / دیاگرام معماری

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                       MAAT ARCHITECTURE — LOGICAL VIEW                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ┌──────────────────────────────────────────────────────────────────────┐   ║
║  │  LAYER 1 — CORE  [Isolated VLAN]                                     │   ║
║  │  DNS Resolver | Log Aggregator | Metrics Collector | Secrets Manager  │   ║
║  │  (Example tools: dns-recursor, OpenSearch, Fluentd, Prometheus, Vault)│   ║
║  └───────────────────────────────▲──────────────────────────────────────┘   ║
║                                  │ ← ALL services connect here (log+metrics) ║
║  ┌─────────────────┐  ┌──────────┴──────────┐  ┌───────────────────────┐   ║
║  │  LAYER 2        │  │  LAYER 3            │  │  LAYER 5              │   ║
║  │  DATABASE       │  │  PUBLIC SERVICES    │  │  FILE STORAGE         │   ║
║  │  [Isolated VLAN]│  │  [Isolated VLAN]    │  │  [Isolated VLAN]      │   ║
║  │                 │  │  Auth | AuthZ | IAM │  │  Object/File Storage  │   ║
║  │  Primary DB     │  │  UserMgmt | Config  │  │                       │   ║
║  │  DB Proxy       │  │  Cache | OTP | Cron │  │                       │   ║
║  │  (Legacy DB)    │  │  Payment | Captcha  │  │                       │   ║
║  └────────▲────────┘  └──────────▲──────────┘  └───────────▲───────────┘   ║
║           │                      │                          │                ║
║  ┌────────┴──────────────────────┴──────────────────────────┴─────────────┐ ║
║  │  LAYER 6 — PROJECT SERVICES  [Isolated VLAN per project]               │ ║
║  │  Service A | Service B | Service C | Project Cache | ...               │ ║
║  │  (number and type defined per project — only layer with variable size) │ ║
║  └───────────────────────────────▲───────────────────────────────────────┘  ║
║                                  │ ← only explicitly allowed connections     ║
║  ┌───────────────────────────────┴───────────────────────────────────────┐   ║
║  │  LAYER 4 — GATEWAY  [Isolated VLAN]                                   │   ║
║  │  ► Authentication enforced here                                       │   ║
║  │  ► Authorization enforced here                                        │   ║
║  │  ► Single entry point — NO bypass allowed                             │   ║
║  └───────────────────────────────▲───────────────────────────────────────┘   ║
╚═════════════════════════════════╪═════════════════════════════════════════════╝
                                  │
                         [External Client]
                         
  OUTBOUND:  [Project Services] → [Egress Gateway per ext. system] → [External]
  X-PROJECT: [Project A]        → [Project B Gateway]              → [Project B]
```

---

## 10. Tooling Reference / ابزارهای مرجع

> ابزارهای زیر از پیاده‌سازی‌های فعلی سازمان استخراج شده‌اند و **نمونه** هستند، نه الزام.  
> Tools below are extracted from current organizational implementations and are **examples**, not requirements.

| Layer | Concept | Current Example | Replaceable With |
|-------|---------|-----------------|-----------------|
| Core | DNS | dns-recursor, dns-authoritative | CoreDNS, BIND, Route53 |
| Core | Logging | OpenSearch, Fluentd | ELK Stack, Loki, Datadog |
| Core | Monitoring | Prometheus, Grafana | Datadog, VictoriaMetrics |
| Core | Secrets | Vault | AWS Secrets Manager, Doppler |
| Database | Primary Store | Atlas 4, PostgreSQL | Any RDBMS or NoSQL |
| Database | Legacy Store | DLS | Any legacy-compatible store |
| Database | DB Proxy | gateway-pg | PgBouncer, ProxySQL |
| Public Services | Authentication | authentication service | Keycloak, Auth0, custom |
| Public Services | Authorization | authorization service | OPA, Casbin, custom |
| Public Services | IAM | Samad | Keycloak, custom IAM |
| Public Services | Config | CCS / configManagement | Consul, Spring Config, Vault |
| Public Services | Cache | Redis | Memcached, Dragonfly |
| Gateway | API Gateway | Gateway service | Kong, Nginx, Envoy, Traefik |
| File Storage | Object Store | filestorage service | MinIO, S3, Ceph |
| Internal Proxy | Service Proxy | TBD (not yet standardized) | Nginx, Envoy, Traefik |

---
