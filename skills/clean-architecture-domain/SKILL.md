---
name: clean-architecture-domain
description: Design and implement pure Domain Layer components (Entities, Value Objects, Domain Events, Aggregate Roots, Repository Interfaces) free from framework dependencies.
tags:
  - both
  - backend
  - frontend
---

# Clean Architecture Domain Layer Skill

Use this skill when designing, creating, or modifying components inside the **Domain Layer** (`src/domain`).

---

## 🎯 Primary Responsibilities

1. Build **Rich Domain Entities** that encapsulate business rules and protect invariants (avoiding Anemic Domain Models).
2. Create immutable **Value Objects** for attributes requiring validation, equality by value, and self-contained behavior.
3. Define **Domain Events** to notify other parts of the system when significant business state transitions occur.
4. Declare **Repository Interfaces (Contracts)** that specify what domain persistence operations are needed, without any database technology leak.

---

## 🏗️ Domain Component Guidelines

### 1. Entities & Aggregate Roots
- Must have unique identity (e.g., `UUID`, `Id` value object).
- Must protect their internal state with methods reflecting business verbs (e.g., `user.changePassword(...)`, `order.cancel(...)`, `account.withdraw(...)`), NOT generic setters.
- Must validate business rules on creation and state mutation.

### 2. Value Objects
- Identified solely by their properties, not an ID.
- Must be **immutable** (any change returns a new instance).
- Examples: `Email`, `Money`, `Address`, `PasswordHash`, `DateRange`, `PhoneNumber`.

### 3. Domain Events
- Represent past business occurrences (named in past tense, e.g., `UserRegisteredEvent`, `OrderPlacedEvent`, `PaymentFailedEvent`).
- Carry relevant domain state and timestamp.

### 4. Repository Interfaces
- Placed in `src/domain/repositories/`.
- Speak the domain ubiquitous language (e.g., `save(user: User)`, `findByEmail(email: Email)`).
- Never return or accept database-specific DTOs, ORM rows, or HTTP payloads. Only Domain Entities and Value Objects.

---

## 🚫 Domain Layer Guardrails

- ❌ **NO ORM Decorators/Imports**: Never import `@Entity()`, `@Column()`, Prisma client, Mongoose, or TypeORM in the Domain.
- ❌ **NO Web/HTTP Concepts**: Never use `Request`, `Response`, HTTP status codes, or web cookies in the Domain.
- ❌ **NO I/O or External Calls**: Domain methods must be deterministic pure business calculations. Any I/O must be orchestrated by the Application Layer.

---

## 📚 Further Reference

See [domain-patterns.md](references/domain-patterns.md) for code templates and pattern examples.
