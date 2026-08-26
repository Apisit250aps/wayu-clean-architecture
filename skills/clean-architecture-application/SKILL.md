---
name: clean-architecture-application
description: Implement Application Layer business use cases, interactors, CQRS commands/queries, DTOs, ports, and mappers.
---

# Clean Architecture Application Layer Skill

Use this skill when building features, workflows, and business use cases in the **Application Layer** (`src/application`).

---

## 🎯 Primary Responsibilities

1. **Single Responsibility Use Cases / Interactors**: Each use case executes exactly one business action (e.g., `RegisterUserUseCase`, `ChangePasswordUseCase`, `CreateOrderUseCase`).
2. **Define Input & Output DTOs**: Never expose internal domain entities directly across boundary layers; map through explicit DTOs.
3. **Declare Application Ports (Interfaces)**: Define contracts for cross-cutting external services (e.g., `ITokenService`, `IEmailService`, `IPaymentGateway`, `IIdGenerator`).
4. **Data Mappers**: Convert between Domain Entities and Application DTOs cleanly.

---

## 🏗️ Use Case Anatomy & Workflow

Every Use Case should follow a standard orchestration flow:

```text
[Input DTO] ──▶ [Validate & Parse VOs] ──▶ [Fetch Domain Entities via Repo Interface]
                                                         │
                                                         ▼
[Output DTO] ◀── [Map Result] ◀── [Persist / Dispatch] ◀── [Execute Domain Logic]
```

### Standard Execution Steps
1. Receive input DTO from Presentation layer.
2. Construct Domain Value Objects (which enforces invariant validation).
3. Query domain repository or external ports for needed aggregates.
4. Call business methods on the Domain Entity.
5. Save updated state through the repository interface.
6. Dispatch domain events or external notifications via ports.
7. Return a response DTO (or void / Result object) back to the caller.

---

## 🚫 Application Layer Guardrails

- ❌ **NO Concrete Infrastructure Dependencies**: Never import `PrismaClient`, `TypeORM`, `axios`, `nodemailer`, or `ioredis`. Only import interface ports.
- ❌ **NO HTTP/Web Specifics**: Never accept `express.Request`, `res: Response`, `next`, or HTTP headers into a Use Case.
- ❌ **NO Business Logic Duplication**: Core business validation belongs in Domain Entities/Value Objects, not scattered across use cases.

---

## 📚 Further Reference

See [usecase-patterns.md](references/usecase-patterns.md) for code patterns, DTOs, and Port definitions.
