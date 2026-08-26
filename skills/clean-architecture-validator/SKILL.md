---
name: clean-architecture-validator
description: Audit and validate existing codebases to detect Clean Architecture violations, layer leaks, improper imports, and bypassed use cases.
tags:
  - both
  - fullstack
---

# Clean Architecture Validator & Auditor Skill

Use this skill to review, audit, and diagnose existing projects for Clean Architecture compliance.

---

## 🎯 Primary Responsibilities

1. **Detect Layer Leaks**: Identify when inner layers (Domain, Application) import from outer layers (Infrastructure, Presentation) or third-party frameworks.
2. **Find Bypassed Use Cases**: Identify when Presentation controllers query DB repositories directly instead of going through Application use cases.
3. **Inspect Domain Purity**: Ensure Entities and Value Objects do not contain ORM annotations, database queries, or HTTP constructs.
4. **Produce Actionable Refactoring Plans**: Provide clear, step-by-step refactoring steps to fix architectural debt.

---

## 🔍 Layer Audit Checklist

| Layer | Check Item | Permitted | Prohibited |
| :--- | :--- | :--- | :--- |
| **Domain** | Imports | Language primitives, internal domain files. | Express, Fastify, Prisma, TypeORM, Axios, Application DTOs. |
| **Domain** | Entity Design | Business logic methods, encapsulation, invariant checks. | Public setters for everything, DB column decorators. |
| **Application** | Imports | Domain entities/VOs/interfaces, other application DTOs/ports. | PrismaClient, TypeORM repos, Express Request/Response. |
| **Application** | Use Cases | Single responsibility orchestration. | Multi-thousand line monolithic god classes. |
| **Presentation** | Controller Dependencies | Application Use Cases. | Concrete Database Repositories, raw SQL queries. |
| **Infrastructure**| Interface Implementation | Implements Domain/App interfaces, maps to Domain entities. | Returning raw ORM instances directly across boundaries. |

---

## 🚀 How to Conduct an Architectural Audit

1. **Analyze Package & Import Graphs**:
   - Check all `import` / `require` / `use` statements in `src/domain` and `src/application`.
2. **Review Controllers**:
   - Inspect constructor parameters of Controllers. If a Repository is injected instead of a Use Case, flag as a violation.
3. **Inspect Models vs Entities**:
   - Verify if Domain entities are independent of database tables.
4. **Generate Report**:
   - List each violation with file path, line number, violation description, and suggested fix.

---

## 📚 Further Reference

See [validation-checklist.md](references/validation-checklist.md) for detailed audit scoring and red flags.
