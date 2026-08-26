# Domain Layer Patterns & Code Templates

## 1. Value Object Pattern (TypeScript)

```typescript
// src/domain/value-objects/email.vo.ts
export class Email {
  private readonly value: string;

  private constructor(value: string) {
    this.value = value;
  }

  public static create(rawEmail: string): Email {
    if (!rawEmail || !rawEmail.includes('@') || !rawEmail.includes('.')) {
      throw new Error(`Invalid email address: ${rawEmail}`);
    }
    return new Email(rawEmail.toLowerCase().trim());
  }

  public getValue(): string {
    return this.value;
  }

  public equals(other: Email): boolean {
    return this.value === other.getValue();
  }
}
```

---

## 2. Rich Entity Pattern (TypeScript)

```typescript
// src/domain/entities/user.entity.ts
import { Email } from '../value-objects/email.vo';

export class User {
  private constructor(
    public readonly id: string,
    private name: string,
    private email: Email,
    private isActive: boolean,
    public readonly createdAt: Date
  ) {}

  public static create(id: string, name: string, email: Email): User {
    if (!name || name.trim().length < 2) {
      throw new Error('User name must be at least 2 characters.');
    }
    return new User(id, name, email, true, new Date());
  }

  public static reconstitute(
    id: string,
    name: string,
    email: Email,
    isActive: boolean,
    createdAt: Date
  ): User {
    return new User(id, name, email, isActive, createdAt);
  }

  public updateName(newName: string): void {
    if (!newName || newName.trim().length < 2) {
      throw new Error('Invalid user name.');
    }
    this.name = newName.trim();
  }

  public deactivate(): void {
    this.isActive = false;
  }

  public getName(): string {
    return this.name;
  }

  public getEmail(): Email {
    return this.email;
  }

  public getIsActive(): boolean {
    return this.isActive;
  }
}
```

---

## 3. Domain Event Pattern

```typescript
// src/domain/events/user-registered.event.ts
export class UserRegisteredEvent {
  public readonly occurredAt: Date;

  constructor(
    public readonly userId: string,
    public readonly email: string
  ) {
    this.occurredAt = new Date();
  }
}
```

---

## 4. Repository Interface Contract

```typescript
// src/domain/repositories/user.repository.interface.ts
import { User } from '../entities/user.entity';
import { Email } from '../value-objects/email.vo';

export interface IUserRepository {
  findById(id: string): Promise<User | null>;
  findByEmail(email: Email): Promise<User | null>;
  save(user: User): Promise<void>;
  delete(id: string): Promise<void>;
}
```
