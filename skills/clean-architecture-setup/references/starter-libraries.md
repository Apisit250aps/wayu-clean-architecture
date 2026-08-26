# Custom Starter Libraries & Utilities (Clean Architecture Toolkit) 🧰

This reference provides the battle-tested custom libraries and utilities extracted from production Clean Architecture projects. When scaffolding or setting up a new project, use these ready-to-use implementations.

---

## 📦 Table of Contents
1. [Domain: Zod Entity Builder (`lib/entity.ts`)](#1-domain-zod-entity-builder-libentityts)
2. [Domain: Base Contracts (`BaseUseCase` & `BaseRepository`)](#2-domain-base-contracts-baseusecase--baserepository)
3. [Application: App Errors & API Response (`lib/error.ts`)](#3-application-app-errors--api-response-liberrorts)
4. [Database: Drizzle Generic Base Repository (`repository.ts`)](#4-database-drizzle-generic-base-repository-repositoryts)
5. [Database: Schema Helpers & UUIDv7 (`lib/utils.ts` & `lib/uuid.ts`)](#5-database-schema-helpers--uuidv7-libutilsts--libuuidts)
6. [Infrastructure: Argon2 Password Hasher (`lib/password.ts`)](#6-infrastructure-argon2-password-hasher-libpasswordts)
7. [Tools: TypeSpec Generator with ts-morph (`scripts/generate.ts`)](#7-tools-typespec-generator-with-ts-morph-scriptsgeneratets)

---

## 1. Domain: Zod Entity Builder (`lib/entity.ts`)

A type-safe utility for building Domain Entities and Schemas with UUIDv7, timestamps, nullable/optional helpers, and default values.

```typescript
// packages/domains/src/lib/entity.ts or src/domain/lib/entity.ts
import { core, util, z } from 'zod';
import { v7 as uuidv7 } from 'uuid';

type BaseFieldOptions<T> = {
  required?: boolean;
  nullable?: boolean;
  default?: util.NoUndefined<core.output<T>> | (() => T);
};

type FieldResult<
  TSchema extends z.ZodTypeAny,
  TRequired extends boolean,
  TNullable extends boolean,
> = TNullable extends true
  ? TRequired extends false
    ? z.ZodNullable<z.ZodOptional<TSchema>>
    : z.ZodNullable<TSchema>
  : TRequired extends false
    ? z.ZodOptional<TSchema>
    : TSchema;

type StringFieldOptions = BaseFieldOptions<string>;
type EmailFieldOptions = BaseFieldOptions<string>;
type UUIDFieldOptions = BaseFieldOptions<string>;
type NumberFieldOptions = BaseFieldOptions<number>;
type DateFieldOptions = BaseFieldOptions<Date>;
type BooleanFieldOptions = BaseFieldOptions<boolean>;

const createField = <
  TSchema extends z.ZodTypeAny,
  TRequired extends boolean = true,
  TNullable extends boolean = false,
>(
  schema: TSchema,
  options: BaseFieldOptions<z.input<TSchema>> & {
    required?: TRequired;
    nullable?: TNullable;
  } = {},
): FieldResult<TSchema, TRequired, TNullable> => {
  const { required = true as TRequired, nullable = false as TNullable } =
    options;
  let result: z.ZodTypeAny = schema;

  if (!required) {
    result = result.optional();
  }

  if (nullable) {
    result = result.nullable();
  }

  if (options.default !== undefined) {
    result = result.default(options.default).unwrap();
  }

  return result as FieldResult<TSchema, TRequired, TNullable>;
};

const StringField = <
  TRequired extends boolean = true,
  TNullable extends boolean = false,
>(
  options: StringFieldOptions & {
    required?: TRequired;
    nullable?: TNullable;
    max?: number;
    min?: number;
  } = {},
) => {
  const base = z
    .string()
    .max(options.max ?? 255)
    .min(options.min ?? 0)
    .trim();
  const schema = options.required === false ? base : base.nonempty();
  return createField(schema, options);
};

const UUIDField = <
  TRequired extends boolean = true,
  TNullable extends boolean = false,
>(
  options: UUIDFieldOptions & {
    required?: TRequired;
    nullable?: TNullable;
  } = {},
) => {
  return createField(z.uuid(), options);
};

const EmailField = <
  TRequired extends boolean = true,
  TNullable extends boolean = false,
>(
  options: EmailFieldOptions & {
    required?: TRequired;
    nullable?: TNullable;
  } = {},
) => {
  return createField(z.email().trim().max(320), options);
};

const NumberField = <
  TRequired extends boolean = true,
  TNullable extends boolean = false,
>(
  options: NumberFieldOptions & {
    required?: TRequired;
    nullable?: TNullable;
  } = {},
) => {
  return createField(z.number(), options);
};

const DateField = <
  TRequired extends boolean = true,
  TNullable extends boolean = false,
>(
  options: DateFieldOptions & {
    required?: TRequired;
    nullable?: TNullable;
  } = {},
) => {
  return createField(z.date(), options);
};

const TimestampField = () => {
  return DateField({ default: () => new Date() });
};

const BooleanField = <
  TRequired extends boolean = true,
  TNullable extends boolean = false,
>(
  options: BooleanFieldOptions & {
    required?: TRequired;
    nullable?: TNullable;
  } = {},
) => {
  return createField(z.boolean(), options);
};

const BaseEntity = <T extends z.ZodRawShape>(schema: T) => {
  return z.object({
    id: UUIDField({ default: () => uuidv7() }),
    ...schema,
    createdAt: TimestampField(),
    updatedAt: TimestampField(),
  });
};

export {
  BaseEntity,
  StringField,
  EmailField,
  UUIDField,
  NumberField,
  DateField,
  BooleanField,
  TimestampField,
  uuidv7 as uuid,
};
```

---

## 2. Domain: Base Contracts (`BaseUseCase` & `BaseRepository`)

```typescript
// packages/domains/src/index.ts or src/domain/index.ts
export abstract class BaseUseCase<Context, TOutput> {
  abstract execute(context: Context): Promise<TOutput>;
}

export abstract class BaseRepository<T, Create, Update> {
  abstract findAll(): Promise<T[]>;
  abstract findById(id: string): Promise<T | null>;
  abstract create(entity: Create): Promise<T>;
  abstract update(id: string, entity: Update): Promise<T>;
  abstract delete(id: string): Promise<void>;
}
```

---

## 3. Application: App Errors & API Response (`lib/error.ts`)

A standardized error hierarchy and response envelope for applications and presentation layers.

```typescript
// packages/applications/src/lib/error.ts or src/application/lib/error.ts
type AppErrorCode =
  | 'NOT_FOUND'
  | 'VALIDATION_ERROR'
  | 'INTERNAL_ERROR'
  | 'UNAUTHORIZED'
  | 'FORBIDDEN';

class AppError extends Error {
  constructor(
    message: string,
    public readonly statusCode: number = 500,
    public readonly code?: AppErrorCode,
  ) {
    super(message);
    this.name = 'AppError';
  }
}

class NotFoundError extends AppError {
  constructor(message = 'Not Found') {
    super(message, 404, 'NOT_FOUND');
    this.name = 'NotFoundError';
  }
}

class ValidationError extends AppError {
  constructor(message = 'Validation Error') {
    super(message, 400, 'VALIDATION_ERROR');
    this.name = 'ValidationError';
  }
}

class InternalError extends AppError {
  constructor(message = 'Internal Server Error') {
    super(message, 500, 'INTERNAL_ERROR');
    this.name = 'InternalError';
  }
}

class UnauthorizedError extends AppError {
  constructor(message = 'Unauthorized') {
    super(message, 401, 'UNAUTHORIZED');
    this.name = 'UnauthorizedError';
  }
}

class ForbiddenError extends AppError {
  constructor(message = 'Forbidden') {
    super(message, 403, 'FORBIDDEN');
    this.name = 'ForbiddenError';
  }
}

class DuplicateError extends AppError {
  constructor(message = 'Duplicate') {
    super(message, 409, 'VALIDATION_ERROR');
    this.name = 'DuplicateError';
  }
}

type ApiResponse<T> = {
  message: string;
  success: boolean;
  data?: T;
  error?: string;
  code?: AppErrorCode;
};

const throwAppError = (error: unknown): never => {
  if (error instanceof AppError) {
    throw error;
  }
  throw new InternalError(
    error instanceof Error ? error.message : 'Unknown error',
  );
};

export {
  AppError,
  NotFoundError,
  ValidationError,
  InternalError,
  UnauthorizedError,
  ForbiddenError,
  DuplicateError,
  throwAppError,
};

export type { AppErrorCode, ApiResponse };
```

---

## 4. Database: Drizzle Generic Base Repository (`repository.ts`)

Provides automated CRUD implementations for all repositories using Drizzle ORM.

```typescript
// packages/database/src/repository.ts or src/infrastructure/database/repository.ts
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

## 5. Database: Schema Helpers & UUIDv7 (`lib/utils.ts` & `lib/uuid.ts`)

```typescript
// packages/database/src/lib/uuid.ts
import { v7 as uuidv7 } from 'uuid';

export const generateUUID = () => uuidv7();
```

```typescript
// packages/database/src/lib/utils.ts
import { uuid, timestamp } from 'drizzle-orm/pg-core';
import { generateUUID } from './uuid';

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

## 6. Infrastructure: Argon2 Password Hasher (`lib/password.ts`)

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

---

## 7. Tools: TypeSpec Generator with ts-morph (`scripts/generate.ts`)

Automatically generates TypeSpec (`.tsp`) models from TypeScript Domain Entities for OpenAPI/Client generation.

```typescript
// packages/domains/scripts/generate.ts
import { Project } from 'ts-morph';
import path from 'path';
import fs from 'fs';
import { log } from 'console';

const root = process.cwd();

function tsTypeToTsp(typeName: string): string {
  const t = typeName.trim();
  if (t.includes('|')) {
    return t
      .split('|')
      .map((subType) => tsTypeToTsp(subType.trim()))
      .join(' | ');
  }
  if (t.endsWith('[]')) {
    const inner = t.slice(0, -2);
    return `${tsTypeToTsp(inner)}[]`;
  }
  switch (t) {
    case 'string': return 'string';
    case 'number': return 'int32';
    case 'boolean': return 'boolean';
    case 'Date': return 'utcDateTime';
    case 'null': return 'null';
    default: return t;
  }
}

function buildModelBlock(
  name: string,
  props: { name: string; optional: boolean; typeText: string }[],
): string {
  const lines: string[] = [];
  lines.push(`  model ${name} {`);

  const BASE_FIELDS = ['id', 'createdAt', 'updatedAt', 'deletedAt'];
  const hasBaseFields = props.some((p) => BASE_FIELDS.includes(p.name));
  const domainProps = props.filter((p) => !BASE_FIELDS.includes(p.name));

  if (hasBaseFields) {
    lines.push(`    ...BaseEntity;`);
    if (domainProps.length > 0) lines.push('');
  }

  for (const prop of domainProps) {
    const tspType = tsTypeToTsp(prop.typeText);
    lines.push(`    ${prop.name}${prop.optional ? '?' : ''}: ${tspType};`);
  }

  lines.push('  }');
  return lines.join('\n');
}

const SKIP_PROPS = new Set(['schema']);
const entitiesGlob = path.join(root, 'src/entities/**/*.ts');
const outPath = path.join(root, '../../packages/client/spec/models/entities.tsp');

const project = new Project({
  tsConfigFilePath: path.join(root, 'tsconfig.json'),
  skipAddingFilesFromTsConfig: true,
});

project.addSourceFilesAtPaths(entitiesGlob);
fs.mkdirSync(path.dirname(outPath), { recursive: true });

const blocks: string[] = [];

for (const sourceFile of project.getSourceFiles()) {
  for (const en of sourceFile.getEnums()) {
    const enumName = en.getName();
    if (!enumName) continue;
    const lines: string[] = [];
    lines.push(`  enum ${enumName} {`);
    for (const member of en.getMembers()) {
      const memberName = member.getName();
      const value = member.getValue();
      lines.push(
        typeof value === 'string'
          ? `    ${memberName}: "${value}",`
          : `    ${memberName}: ${value},`
      );
    }
    lines.push('  }');
    blocks.push(lines.join('\n'));
  }

  for (const cls of sourceFile.getClasses()) {
    const className = cls.getName();
    if (!className) continue;
    const props = cls
      .getProperties()
      .filter((p) => !SKIP_PROPS.has(p.getName()))
      .map((p) => ({
        name: p.getName(),
        optional: p.hasQuestionToken(),
        typeText: p.getTypeNode()?.getText() ?? p.getType().getText(p),
      }));
    blocks.push(buildModelBlock(`${className}`, props));
  }
}

const baseEntityTemplate = `  model BaseEntity {\n    id: string;\n    createdAt: utcDateTime;\n    updatedAt: utcDateTime;\n  }`;
const finalTspContent = `namespace Domain.Entity;\n\n${baseEntityTemplate}\n\n${blocks.join('\n\n')}\n`;

fs.writeFileSync(outPath, finalTspContent, 'utf-8');
log(`Generated TypeSpec: ${outPath}`);
```
