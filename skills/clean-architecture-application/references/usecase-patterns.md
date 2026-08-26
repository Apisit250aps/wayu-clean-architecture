# Application Layer Patterns & Code Templates

## 1. Input / Output DTO Pattern

```typescript
// src/application/dtos/register-user.dto.ts
export interface RegisterUserInputDto {
  name: string;
  email: string;
}

export interface RegisterUserOutputDto {
  id: string;
  name: string;
  email: string;
  createdAt: string;
}
```

---

## 2. Application Port (External Service Interface)

```typescript
// src/application/ports/email-service.port.ts
export interface IEmailService {
  sendWelcomeEmail(toEmail: string, userName: string): Promise<void>;
}
```

```typescript
// src/application/ports/id-generator.port.ts
export interface IIdGenerator {
  generate(): string;
}
```

---

## 3. Use Case / Interactor Implementation

```typescript
// src/application/use-cases/register-user.usecase.ts
import { User } from '../../domain/entities/user.entity';
import { Email } from '../../domain/value-objects/email.vo';
import { IUserRepository } from '../../domain/repositories/user.repository.interface';
import { IEmailService } from '../ports/email-service.port';
import { IIdGenerator } from '../ports/id-generator.port';
import { RegisterUserInputDto, RegisterUserOutputDto } from '../dtos/register-user.dto';

export class RegisterUserUseCase {
  constructor(
    private readonly userRepo: IUserRepository,
    private readonly emailService: IEmailService,
    private readonly idGenerator: IIdGenerator
  ) {}

  async execute(input: RegisterUserInputDto): Promise<RegisterUserOutputDto> {
    const email = Email.create(input.email);

    const existingUser = await this.userRepo.findByEmail(email);
    if (existingUser) {
      throw new Error('A user with this email already exists.');
    }

    const userId = this.idGenerator.generate();
    const newUser = User.create(userId, input.name, email);

    await this.userRepo.save(newUser);
    await this.emailService.sendWelcomeEmail(newUser.getEmail().getValue(), newUser.getName());

    return {
      id: newUser.id,
      name: newUser.getName(),
      email: newUser.getEmail().getValue(),
      createdAt: newUser.createdAt.toISOString(),
    };
  }
}
```
