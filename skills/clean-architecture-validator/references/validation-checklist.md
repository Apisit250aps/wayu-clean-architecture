# Clean Architecture Validation Checklist & Red Flags

## 🚩 Top Red Flags in Clean Architecture

### 1. The Anemic Domain Anti-Pattern
- **Violation**: Entities are just plain data bags with getters and setters, and all business rules are placed in Use Cases or Service classes.
- **Remedy**: Move entity-specific business logic and invariant validation directly into the Entity.

### 2. The Direct DB Controller Anti-Pattern
- **Violation**: HTTP controllers inject Prisma/TypeORM/GORM directly and perform database updates inside controller route handlers.
- **Remedy**: Encapsulate the operation in an Application Use Case, and have the controller invoke the Use Case.

### 3. The ORM Leak Anti-Pattern
- **Violation**: Domain entities have `@Column()` or `@Entity()` decorators, or Use Cases return Prisma-generated models to the Presentation layer.
- **Remedy**: Separate persistence schema (`infrastructure/database/models`) from Domain Entities (`domain/entities`), and use a mapper class in Infrastructure.

### 4. Direct Outer-Layer Imports in Domain
- **Violation**: `import { RegisterUserDto } from '../application/dtos/register-user.dto'` inside `src/domain/entities/user.entity.ts`.
- **Remedy**: Domain must never import from Application, Infrastructure, or Presentation.
