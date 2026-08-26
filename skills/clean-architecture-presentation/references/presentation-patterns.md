# Presentation Layer Patterns & Code Templates

## 1. Express Controller Pattern (TypeScript)

```typescript
// src/presentation/http/controllers/register-user.controller.ts
import { Request, Response, NextFunction } from 'express';
import { RegisterUserUseCase } from '../../../application/use-cases/register-user.usecase';
import { z } from 'zod';

const registerUserSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
});

export class RegisterUserController {
  constructor(private readonly registerUserUseCase: RegisterUserUseCase) {}

  async handle(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const parsedBody = registerUserSchema.parse(req.body);

      const result = await this.registerUserUseCase.execute({
        name: parsedBody.name,
        email: parsedBody.email,
      });

      res.status(201).json({
        success: true,
        data: result,
      });
    } catch (error: any) {
      if (error instanceof z.ZodError) {
        res.status(400).json({
          success: false,
          errors: error.errors.map((e) => ({ field: e.path.join('.'), message: e.message })),
        });
        return;
      }
      next(error);
    }
  }
}
```

---

## 2. Global Error Handling Middleware

```typescript
// src/presentation/http/middlewares/error-handler.middleware.ts
import { Request, Response, NextFunction } from 'express';

export function errorHandler(
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
): void {
  // Domain/Application error mapping
  if (err.message.includes('already exists')) {
    res.status(409).json({ success: false, error: err.message });
    return;
  }

  if (err.message.includes('not found')) {
    res.status(404).json({ success: false, error: err.message });
    return;
  }

  console.error('Unhandled server error:', err);
  res.status(500).json({
    success: false,
    error: 'Internal Server Error',
  });
}
```
