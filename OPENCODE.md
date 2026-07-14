# Prism Intelligence - OpenCode Configuration

## Coding Rules

### Architecture (MANDATORY - Never Violate)

1. **Clean Architecture (Ports & Adapters)**
   - `domain` CANNOT import from `application`, `infrastructure`, or `interfaces`
   - `application` CANNOT import from `infrastructure` or `interfaces`
   - `infrastructure` implements `application` ports (interfaces)
   - `interfaces` uses `application` services
   - Dependencies point INWARD only

2. **Lightweight DDD with Bounded Contexts**
   - Four bounded contexts: `portfolio`, `market`, `analytics`, `risk`
   - Each context: `entities`, `value_objects`, `events`, `repositories`, `services`
   - Contexts communicate via domain events only
   - Shared kernel in `domain.shared` only

3. **Plugin-Based Market Extensibility**
   - Market data providers implement `MarketDataProvider` port
   - New providers added without modifying core domain
   - Adapters in `infrastructure.market_data.adapters`

4. **Independent Engines**
   - Ingestion, Backtesting, Portfolio, Risk engines are separate
   - Each engine has its own application service
   - Communicate via domain events

### Code Quality

1. **Type Hints Everywhere**
   - All function signatures must have type hints
   - Use `typing` module: `Annotated`, `Protocol`, `TypeVar`, `Generic`
   - No `Any` unless absolutely necessary with comment

2. **Tests for Domain Logic**
   - Every domain entity, value object, service must have tests
   - Unit tests in `tests/unit/domain/`
   - Use property-based testing for value objects
   - Test domain events and invariants

3. **Formatting: Black + Ruff**
   - Line length: 100
   - Double quotes
   - Run `ruff check . && ruff format .` before commit
   - Run `mypy src/prism` for type checking

### Import Rules (Enforced by import-linter)

```ini
# domain -> application, infrastructure, interfaces (FORBIDDEN)
# application -> infrastructure, interfaces (FORBIDDEN)
# infrastructure -> interfaces (ALLOWED, implements ports)
# interfaces -> application (ALLOWED, uses services)
```

### Naming Conventions

- Classes: `PascalCase`
- Functions/Methods: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private: `_leading_underscore`
- Type variables: `T`, `T_co`, `T_contra`
- Protocols: `*Protocol` suffix

### Project Structure

```
src/prism/
├── domain/              # Pure domain logic (NO external deps)
│   ├── portfolio/
│   ├── market/
│   ├── analytics/
│   ├── risk/
│   └── shared/
├── application/         # Use cases, ports, DTOs
│   ├── portfolio/
│   ├── market/
│   ├── analytics/
│   └── risk/
├── infrastructure/      # External implementations
│   ├── persistence/
│   ├── market_data/
│   ├── celery/
│   ├── api/
│   └── config/
└── interfaces/          # Entry points
    ├── api/
    ├── cli/
    └── workers/
```

### Commands

```bash
# Format & lint
ruff check . && ruff format .

# Type check
mypy src/prism

# Tests
pytest tests/unit -v
pytest tests/integration -v
pytest tests/e2e -v

# Import validation
import-linter

# All checks
ruff check . && ruff format . && mypy src/prism && import-linter && pytest tests/unit -v
```

### Pre-commit Hooks

Install: `pre-commit install`

Checks run automatically:
- ruff (lint + format)
- mypy (types)
- import-linter (architecture)
- pytest (unit tests)

### Forbidden Patterns

- ❌ `from prism.infrastructure import ...` in domain/application
- ❌ `from prism.interfaces import ...` in domain/application/infrastructure
- ❌ Direct SQLAlchemy models in domain
- ❌ `async def` without `await` or proper async context
- ❌ Mutable default arguments
- ❌ `except:` bare except
- ❌ Business logic in API routes
- ❌ Circular imports between bounded contexts

### Required Patterns

- ✅ Domain events for cross-context communication
- ✅ Repository protocols in domain, implementations in infrastructure
- ✅ Pydantic models for API schemas (interfaces)
- ✅ Dependency injection via FastAPI `Depends`
- ✅ Structured logging with `structlog`
- ✅ OpenTelemetry instrumentation