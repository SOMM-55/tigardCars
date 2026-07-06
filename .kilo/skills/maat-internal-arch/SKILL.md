---
name: maat-internal-arch
description: >
  Canonical reference for all MAAT-native (internal) infrastructure components.
  Use this skill whenever you need the official component name, minimum version,
  category, or description for any piece of the MAAT stack — including
  PartFramework, Atlas, Delta, Gateway, PublicServices microservices, gitEvents,
  Darkoob, Kakado, Malak, TarTanak, or Simorgh. Always consult this skill before
  writing any architecture catalog, README, or documentation that references
  internal tooling.
---

# MAAT Internal Architecture Reference (v1.0.0)

All version strings are **minimum versions** unless noted otherwise.

---

## Backend

| Component | Min Version | Description | Alternatives |
|---|---|---|---|
| PartFramework | >=10.19.x | Custom JS backend framework (Express.js-based) | Express.js, NestJS, Fastify |

---

## Database & Data Processing

| Component | Min Version | Description | Alternatives |
|---|---|---|---|
| Atlas | >=4.2.x | Key-value document database (MongoDB-based) | PostgreSQL, MySQL, Redis, Cassandra |
| Delta | >=3.x | Data-processor pipeline (Apache Spark-based) | Apache Flink, Kafka, Airflow, Dask |

---

## Gateway

| Component | Min Version | Description | Alternatives |
|---|---|---|---|
| Gateway | >=2.11.x | Central API gateway for all public-facing traffic | Kong, NGINX, Traefik, Envoy |

---

## Microservices (PublicServices)

| Component | Min Version | Description | Alternatives |
|---|---|---|---|
| authentication | >=7.9.15 | User authentication service | Keycloak, Auth0, Firebase Auth |
| authorization | >=10.15.0 | Permission & policy enforcement | Keycloak, OPA |
| samad | >=8.7.0 | RBAC (role-based access control) | Casbin, OPA, Keycloak |
| payment | >=1.2.3 | Payment processing integration | Stripe, PayPal, BTCPay Server |
| profile | >=7.13.0 | User profile provider service | Keycloak user federation, custom |
| otp | >=1.10.4 | One-time password generation & validation | Twilio, HOTP/TOTP libs |
| cron | >=1.4.16 | Scheduled job runner | Kubernetes CronJobs, Airflow |
| captcha | >=6.6.0 | CAPTCHA challenge service | reCAPTCHA, hCaptcha, Friendly Captcha |
| fileStorage | >=3.16.0 | File storage service | MinIO, Nextcloud |
| ccs | >=3.15.0 | Central config & secrets provider | Consul, etcd, Vault, Spring Cloud Config |

---

## CI (Continuous Integration)

| Component | Min Version | Description | Alternatives |
|---|---|---|---|
| gitEvents | >=7.24.1 | GitLab bot triggered on git events | GitHub Actions, Tekton, Drone |
| Darkoob | 2.4.x | Script runner (Jenkins-based); Workflow IDs: PM2=141, Client PM2=445, CI-KK2=74 | Jenkins, CircleCI, Travis CI |
| Kakado Repo | TBD | Source repository for Kakado artifacts | GitLab, GitHub |
| GitLab | TBD | Source control & CI platform | GitHub, Gitea, Bitbucket |

---

## CD (Continuous Deployment)

| Component | Min Version | Description | Alternatives |
|---|---|---|---|
| kakado | >=4.22 | Internal Docker engine for image build & distribution | Docker, Podman |
| Malak | >=3.0 | Custom cloud orchestration platform (VMs, networking, storage, GPU, datacenter clusters) | OpenStack, Proxmox, Kubernetes operators |
| TarTanak | >=2.20.6 | Firewall & network security layer | nftables, iptables, Calico, AWS Security Groups |
| Simorgh | >=1.5.11 | Kubernetes (K8s) cluster management | Rancher, OpenShift, Nomad |

---

## Usage notes

- When generating a catalog with `answer = internal`, pull **only** from this file.
- When `answer = both`, use this file for the **Component** column and pull alternatives from the `maat-external-arch` skill.
- Never invent version numbers; if a version is unknown, output `TBD`.
