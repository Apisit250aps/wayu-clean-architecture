# Naming & Architectural Boundary Enforcements

## Dependency Cruiser Configuration (`.dependency-cruiser.js`)

To automatically validate architecture on every commit or CI build:

```javascript
module.exports = {
  forbidden: [
    {
      name: 'domain-cannot-depend-on-outer-layers',
      severity: 'error',
      from: { path: '^src/domain' },
      to: { path: '^src/(application|infrastructure|presentation)' }
    },
    {
      name: 'application-cannot-depend-on-infrastructure-or-presentation',
      severity: 'error',
      from: { path: '^src/application' },
      to: { path: '^src/(infrastructure|presentation)' }
    },
    {
      name: 'presentation-cannot-depend-on-infrastructure',
      severity: 'error',
      from: { path: '^src/presentation' },
      to: { path: '^src/infrastructure' }
    }
  ]
};
```
