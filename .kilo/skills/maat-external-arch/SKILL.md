---
name: maat-external-arch
description: >
  Canonical reference for the approved external / open-source stack for MAAT
  projects. Each category has exactly one mandated technology — no alternatives.
  Use this skill whenever you need the approved external component for any
  infrastructure category. Do not suggest or list any technology not present
  in this file.
---

# MAAT External / Open-Source Architecture Reference

> **Policy:** Every category has exactly **one** approved technology.
> No alternatives exist in the external stack — the choice is fixed.
> When generating a catalog with `answer = external`, use each entry as-is
> with `"alternatives": []`.

---

## Backend

| Component | Technology | Description |
|---|---|---|
| backend | Express.js | Lightweight, flexible Node.js web framework |

---

## Database & Data

| Component | Technology | Description |
|---|---|---|
| database | PostgreSQL | ACID-compliant relational database with strong JSON support |

> **Note:** Data pipeline has been removed from the external stack. Do not include a pipeline row.

---

## Gateway

| Component | Technology | Description |
|---|---|---|
| gateway | Traefik | Cloud-native edge router; auto-discovers Docker/K8s services |

---

## Microservices

| Component | Technology | Description |
|---|---|---|
| authentication | Keycloak | Open-source IAM — SSO, OIDC, SAML |
| authorization | Keycloak | Policy-based access control (same Keycloak instance) |
| payment | internal | Payment must use the internal MAAT service — no external provider |
| otp | internal | OTP must use the internal MAAT service — no external provider |
| cron | Kubernetes CronJobs | Native K8s scheduled tasks |
| captcha | Friendly Captcha | Self-hostable, accessible CAPTCHA |
| fileStorage | MinIO | S3-compatible self-hosted object storage |
| secretManagement | Vault | Secrets management & encryption (HashiCorp) |

---

## CI

| Component | Technology | Description |
|---|---|---|
| ci | GitLab CI/CD | Built-in pipelines tightly coupled to GitLab repos |

---

## CD

| Component | Technology | Description |
|---|---|---|
| containerisation | Docker Compose | Multi-container local/production orchestration |
| orchestration | Helm | Kubernetes package manager for release management |
| iac | Ansible | Agentless configuration management & IaC |

> **Note:** Firewall has been removed from the external stack. Do not include a firewall row.

---

## Usage notes

- `payment` and `otp` are marked `internal` — when writing a catalog with
  `answer = external`, render their Technology cell as `internal (MAAT service)`
  and description as the internal service description from `maat-internal-arch`.
- Do **not** add alternatives, suggestions, or notes about other technologies.
- Do **not** include Data Pipeline or Firewall rows — they have been deleted.
- `"alternatives": []` for every entry regardless of catalog mode.
