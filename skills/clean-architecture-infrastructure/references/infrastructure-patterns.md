# Infrastructure Layer Patterns & Code Templates

## 1. Concrete Repository Implementation (Prisma Example)

```typescript
// src/infrastructure/database/repositories/prisma-user.repository.ts
import { PrismaClient } from '@prisma/client';
import { IUserRepository } from '../../../domain/repositories/user.repository.interface';
import { User } from '../../../domain/entities/user.entity';
import { Email } from '../../../domain/value-objects/email.vo';

export class PrismaUserRepository implements IUserRepository {
  constructor(private readonly prisma: PrismaClient) {}

  async findById(id: string): Promise<User | null> {
    const record = await this.prisma.user.findUnique({ where: { id } });
    if (!record) return null;
    return this.toDomain(record);
  }

  async findByEmail(email: Email): Promise<User | null> {
    const record = await this.prisma.user.findUnique({
      where: { email: email.getValue() },
    });
    if (!record) return null;
    return this.toDomain(record);
  }

  async save(user: User): Promise<void> {
    await this.prisma.user.upsert({
      where: { id: user.id },
      update: {
        name: user.getName(),
        email: user.getEmail().getValue(),
        isActive: user.getIsActive(),
      },
      create: {
        id: user.id,
        name: user.getName(),
        email: user.getEmail().getValue(),
        isActive: user.getIsActive(),
        createdAt: user.createdAt,
      },
    });
  }

  async delete(id: string): Promise<void> {
    await this.prisma.user.delete({ where: { id } });
  }

  private toDomain(record: {
    id: string;
    name: string;
    email: string;
    isActive: boolean;
    createdAt: Date;
  }): User {
    return User.reconstitute(
      record.id,
      record.name,
      Email.create(record.email),
      record.isActive,
      record.createdAt
    );
  }
}
```

---

## 2. External Service Adapter (Nodemailer Example)

```typescript
// src/infrastructure/external-services/nodemailer-email.service.ts
import nodemailer, { Transporter } from 'nodemailer';
import { IEmailService } from '../../application/ports/email-service.port';

export class NodemailerEmailService implements IEmailService {
  private transporter: Transporter;

  constructor() {
    this.transporter = nodemailer.createTransport({
      host: process.env.SMTP_HOST || 'localhost',
      port: Number(process.env.SMTP_PORT) || 587,
      auth: {
        user: process.env.SMTP_USER || '',
        pass: process.env.SMTP_PASS || '',
      },
    });
  }

  async sendWelcomeEmail(toEmail: string, userName: string): Promise<void> {
    await this.transporter.sendMail({
      from: '"My Clean App" <no-reply@example.com>',
      to: toEmail,
      subject: 'Welcome to our platform!',
      html: `<p>Hello ${userName}, welcome aboard!</p>`,
    });
  }
}
```

---

## 3. ID Generator Adapter (UUID Example)

```typescript
// src/infrastructure/external-services/uuid-id-generator.service.ts
import { v4 as uuidv4 } from 'uuid';
import { IIdGenerator } from '../../application/ports/id-generator.port';

export class UuidIdGenerator implements IIdGenerator {
  generate(): string {
    return uuidv4();
  }
}
```
