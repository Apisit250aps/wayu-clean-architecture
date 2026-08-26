# Infrastructure Layer Patterns & Code Templates

## 1. Drizzle Generic Base Repository (`database/repository.ts`)

```typescript
// packages/database/src/repository.ts
/* eslint-disable @typescript-eslint/no-explicit-any */
import { BaseRepository } from '@shop/domains';
import type { Database } from './db';
import { PgTable } from 'drizzle-orm/pg-core';
import { eq } from 'drizzle-orm';

export abstract class Repository<
  T,
  C extends Record<string, unknown>,
  U extends Record<string, unknown>,
> extends BaseRepository<T, C, U> {
  constructor(
    protected readonly db: Database,
    protected readonly table: PgTable<any>,
  ) {
    super();
  }

  async create(entity: C): Promise<T> {
    const [result] = await this.db
      .insert(this.table)
      .values(entity)
      .returning();
    return result as T;
  }

  async delete(id: string): Promise<void> {
    await this.db.delete(this.table).where(eq((this.table as any).id, id));
  }

  async findAll(): Promise<T[]> {
    const results = await this.db.select().from(this.table);
    return results as T[];
  }

  async findById(id: string): Promise<T | null> {
    const [result] = await this.db
      .select()
      .from(this.table)
      .where(eq((this.table as any).id, id));
    return (result as T) || null;
  }

  async update(id: string, entity: U): Promise<T> {
    const [result] = await this.db
      .update(this.table)
      .set(entity)
      .where(eq((this.table as any).id, id))
      .returning();
    return result as T;
  }
}
```

---

## 2. Drizzle Schema Helpers & UUIDv7 (`database/lib/utils.ts`)

```typescript
// packages/database/src/lib/utils.ts
import { uuid, timestamp } from 'drizzle-orm/pg-core';
import { v7 as uuidv7 } from 'uuid';

export const generateUUID = () => uuidv7();

export function primaryKeyUuid7<T extends string>(columnName: T) {
  return uuid(columnName)
    .primaryKey()
    .$defaultFn(() => generateUUID());
}

export function updatedAtTimestamp<T extends string>(columnName: T) {
  return timestamp(columnName)
    .$onUpdate(() => new Date())
    .notNull();
}

export function createdAtTimestamp<T extends string>(columnName: T) {
  return timestamp(columnName).defaultNow().notNull();
}
```

---

## 3. Concrete Repository Implementation (`infrastructures/repositories/user.repo.ts`)

```typescript
// packages/infrastructures/src/repositories/user.repo.ts
import type { Database } from '@shop/database/db';
import { User } from '@shop/domains/entities';
import { IUserRepository } from '@shop/domains/repositories/user';
import { user } from '@shop/database/schema';
import { Repository } from '@shop/database/repository';
import { CreateUser, UpdateUser } from '@shop/domains/schema/user';
import { eq } from 'drizzle-orm';

export default class UserRepository
  extends Repository<User, CreateUser, UpdateUser>
  implements IUserRepository
{
  constructor(db: Database) {
    super(db, user);
  }

  async findByEmail(email: string): Promise<User | null> {
    const [result] = await this.db
      .select()
      .from(this.table)
      .where(eq(user.email, email));
    return (result as User) || null;
  }
}
```

---

## 4. Argon2 Password Hasher Adapter (`infrastructures/lib/password.ts`)

```typescript
// packages/infrastructures/src/lib/password.ts
import argon2 from 'argon2';

export const hash = async (password: string): Promise<string> => {
  return argon2.hash(password);
};

export const verify = async ({
  password,
  hash,
}: {
  password: string;
  hash: string;
}): Promise<boolean> => {
  return await argon2.verify(hash, password);
};
```
