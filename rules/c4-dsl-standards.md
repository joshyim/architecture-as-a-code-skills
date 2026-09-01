# Structurizr C4 DSL Standards

Follow these guidelines whenever writing, updating, or reviewing Structurizr DSL architecture files:

## 1. Identifiers & Naming Conventions
- **Stable Identifiers**: Use consistent `camelCase` or descriptive identifiers for systems, containers, components, and personas (e.g. `customerPortal`, `authService`, `userDb`).
- **Preserve Existing Identifiers**: Never rename or delete existing identifiers unless explicitly asked. Structurizr layout coordinates, view includes, and relationship targets depend on stable identifier keys. Renaming will reset diagram layouts.

## 2. Layout & Views
- **Manual vs Auto Layout**: Do not add `autoLayout tb` (or other auto-layout directives) to views unless explicitly requested by the user. Manual layout mode allows users to position diagram boxes interactively in Structurizr Local without their positions being overridden on diagram refresh.
- **Scoping Views**: Create distinct views for distinct levels (System Landscape, System Context, Container, and focused Component views). Avoid crowding all components into a single diagram view.

## 3. Elements and Grouping
- **Deployment & Technology**: Always include technology tags on containers and components (e.g., `technology "PostgreSQL 16"`, `technology "FastAPI / Python"`).
- **Meaningful Groups**: Use `group "Display Name" { ... }` for functional clusters (e.g., `group "Data Ingestion"`, `group "Persistent Storage"`).

## 4. Styling & Tags
- Tag external dependencies with `"external app"`.
- Tag prospective or future components with `"future"` or `"proposed"`.
- Ensure corresponding style definitions exist in `styles/style.dsl` for any custom tags used.

## 5. File Modularization
Keep DSL modularized via Structurizr `!include`:
- `workspace.dsl`: Root file wiring model, views, and styles.
- `models/*.dsl`: Software systems, personas, external systems, and relationships.
- `views/views.dsl`: View definitions.
- `styles/style.dsl`: Visual styling tokens.
