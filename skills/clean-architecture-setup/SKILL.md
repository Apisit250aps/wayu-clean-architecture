---
name: clean-architecture-setup
description: Initialize or scaffold a project with Clean Architecture layers (Domain, Application, Infrastructure, Presentation) and configure dependency inversion rules.
---

# Clean Architecture Setup Skill

Use this skill when scaffolding a new project, setting up directory structures, or configuring layer boundaries for Clean Architecture.

---

## 🎯 Primary Responsibilities

1. Generate a robust, standard Clean Architecture directory structure tailored to the user's language/framework (Node.js/TypeScript, Go, Python, C#/.NET, Java/Kotlin, Rust).
2. Set up Dependency Injection (DI) and composition root mechanisms.
3. Configure layer isolation rules to prevent architectural erosion.

---

## 📁 Standard Directory Structure

When creating or reorganizing a project, use the following layout:

```text
src/
├── domain/                    # Enterprise Business Rules (Entities, Value Objects, Domain Events)
│   ├── entities/              # Rich domain models with business invariants
│   ├── value-objects/         # Immutable value objects
│   ├── events/                # Domain events
│   ├── exceptions/            # Domain-specific business rule exceptions
│   └── repositories/          # Repository interfaces (contracts)
│
├── application/               # Application Business Rules (Use Cases, Workflows)
│   ├── use-cases/             # Interactors / CQRS Commands & Queries
│   ├── dtos/                  # Request / Response Data Transfer Objects
│   ├── ports/                 # Interfaces for external services (Email, Payment, Cache)
│   ├── mappers/               # Data mappers between Domain Entities and DTOs
│   └── exceptions/            # Application-level exceptions (NotFound, Conflict, etc.)
│
├── infrastructure/            # Frameworks, Drivers, and Adapters
│   ├── database/              # DB Clients, ORM models, Migrations
│   │   ├── models/            # Database schema / ORM entities (Prisma, TypeORM, etc.)
│   │   └── repositories/      # Concrete implementations of Domain Repository interfaces
│   ├── external-services/     # Third-party API clients (Stripe, SendGrid, S3)
│   ├── caching/               # Redis or in-memory cache implementations
│   └── config/                # Environment variables and configuration loaders
│
├── presentation/              # Interface Adapters (Web, API, CLI)
│   ├── http/                  # HTTP Server (Express, Fastify, Nest, Gin, FastAPI, etc.)
│   │   ├── controllers/       # Route handlers translating HTTP to Use Cases
│   │   ├── middlewares/       # Auth, Rate Limiting, Error Handling
│   │   ├── routes/            # Route definitions
│   │   └── schemas/           # Input validation schemas (Zod, Joi, Pydantic)
│   └── presenters/            # Formatting output data for clients
│
└── main.ts (or main.go / app.py) # Composition Root: Wires DI and starts the application
```

---

## ⚙️ Step-by-Step Scaffolding Workflow

1. **Identify Language and Framework**:
   - Determine target tech stack (e.g., TypeScript/Node, Go, Python, C#).
   - Choose or confirm the DI mechanism (manual factory wiring, Tsyringe, Inversify, NestJS, wire, dependency-injector).

2. **Create Core Layer Folders**:
   - Build directories for `domain`, `application`, `infrastructure`, and `presentation`.
   - Never create direct circular cross-layer links.

3. **Establish Layer Contracts**:
   - Define base interfaces and abstractions:
     - `Entity<T>` and `ValueObject<T>` base classes (if applicable in OOP languages).
     - Result/Either monad or standard error handling types.
     - `UseCase<TInput, TOutput>` interface contract.

4. **Setup Code Formatting & Linting (Prettier & ESLint)**:
   - Create `.prettierrc` and `.prettierignore` to standardize formatting (`singleQuote: true`, `semi: true`, `tabWidth: 2`, `trailingComma: "all"`).
   - Add `"format"` and `"format:check"` npm scripts.
   - Configure `.dependency-cruiser.cjs` for layer boundary checks.

5. **Setup Composition Root**:
   - Create a single entry point (e.g., `src/main.ts` or `src/container.ts`) where all concrete infrastructure implementations are instantiated and injected into Application Use Cases, and Use Cases are injected into Presentation Controllers.

---

## 🛡️ Non-Negotiable Rules

1. **Zero External Dependencies in Domain**: `src/domain` MUST NOT import external libraries, ORMs (e.g., `@prisma/client`, `typeorm`, `mongoose`), or web frameworks (e.g., `express`, `fastify`).
2. **Ports & Adapters in Application**: `src/application` defines interfaces (ports) for things it needs from the outside world (e.g., `IEmailService`, `ITokenGenerator`), but NEVER imports their concrete implementations.
3. **Infrastructure Implements Interfaces**: `src/infrastructure` implements interfaces declared in `domain/repositories` and `application/ports`.
4. **Presentation Calls Use Cases**: Controllers in `presentation` only call Use Cases in `application`. They MUST NEVER invoke Infrastructure Repositories or DB queries directly.

---

## 📚 Further Reference

- [starter-libraries.md](references/starter-libraries.md): Built-in custom utilities, `lib/entity.ts` Zod builder, `lib/error.ts`, generic `Repository` for Drizzle, UUIDv7 helpers, and Argon2 hasher.
- [architecture-overview.md](references/architecture-overview.md): Deep-dive architectural rules, Monorepo structure, and dependency inversion diagrams.

