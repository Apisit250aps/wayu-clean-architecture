---
name: clean-architecture-infrastructure
description: Implement Infrastructure Layer components (database repositories, ORM adapters, external API clients, message brokers, caching) fulfilling domain and application contracts.
tags:
  - backend
---

# Clean Architecture Infrastructure Layer Skill

Use this skill when implementing adapters, database integrations, third-party clients, or framework drivers in the **Infrastructure Layer** (`src/infrastructure`).

---

## 🎯 Primary Responsibilities

1. **Implement Domain Repository Interfaces**: Write concrete repository classes (using Prisma, TypeORM, Drizzle, SQLx, GORM, EF Core, etc.) that implement contracts from `src/domain/repositories/`.
2. **Implement Application Ports**: Write concrete service adapters (e.g., SendGrid, Nodemailer, Stripe, AWS S3, Redis) fulfilling interfaces from `src/application/ports/`.
3. **Handle Persistence Mapping**: Convert between database database rows / ORM models and pure Domain Entities using explicit mappers.
4. **Isolate Third-Party Failures & Complexity**: Wrap external SDK exceptions into known domain/application exceptions.

---

## 🏗️ Persistence Mapping Strategy

Always decouple Database Models from Domain Entities:

```text
[DB Table / ORM Model] ──(Infrastructure Mapper)──▶ [Pure Domain Entity]
```

- **Persistence Model / Schema**: Optimized for storage, SQL indices, foreign keys, and ORM decorators.
- **Domain Entity**: Optimized for business rules, encapsulation, and domain invariants.
- **Mapper**: Bridges the two without letting ORM types leak into the Domain layer.

---

## 🚫 Infrastructure Layer Guardrails

- ❌ **NEVER Bypass Interfaces**: Always implement an interface declared in `domain/repositories` or `application/ports`.
- ❌ **NEVER Leak ORM types into Domain**: Do not pass Prisma/TypeORM generated types back to Use Cases or Entities. Reconstitute proper Domain Entities.
- ❌ **Keep Configuration Centralized**: Load environment variables via configuration adapters rather than querying `process.env` directly throughout repository code.

---

## 📚 Further Reference

See [infrastructure-patterns.md](references/infrastructure-patterns.md) for concrete examples of Prisma/TypeORM repositories and external service adapters.
