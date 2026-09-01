# Architecture-as-a-Code Skills

Agentic AI skills for generating and maintaining interactive **C4 model architecture diagrams** using [Structurizr DSL](https://docs.structurizr.com/dsl).

---

## Overview

This repository provides skills and rules to initialize and maintain architecture-as-code across multiple AI agent environments (Antigravity, Claude Code, Cursor, Windsurf, Copilot, etc.):

- **[`arch-c4-init`](./skills/arch-c4-init/SKILL.md)**: Initializes a complete C4 Structurizr DSL workspace via a structured architecture interview, generating personas, containers, components, relationships, views, styles, and documentation.
- **[`arch-c4-update`](./skills/arch-c4-update/SKILL.md)**: Updates and synchronizes existing Structurizr DSL files with codebase changes, preserving stable identifiers and manual layouts.
- **[`rules/c4-dsl-standards.md`](./rules/c4-dsl-standards.md)**: Structurizr DSL authoring guidelines (camelCase identifiers, stable IDs, manual layout preservation).
- **[`rules/architecture-sync.md`](./rules/architecture-sync.md)**: Workflow rule triggering C4 model updates when code is ready for review, unit testing, commit, or PR generation.

---

## Configuration (`C4_DESTINATION`)

The skills look for a `C4_DESTINATION` variable in the target project's `.env.dev` file to determine where to output and read DSL files.

Example `.env.dev`:

```env
C4_DESTINATION=docs/architecture
```

If `C4_DESTINATION` is not configured, the skills will prompt you for the destination path.

---

## Installation

You can install and use these skills via either **`uv` / `pip`** (no manual cloning) or as a **Git Submodule** across Antigravity, Claude Code, Cursor, Windsurf, and other agent tools.

### Option 1: Install via `uv` or `pip` (Recommended — Zero Cloning)

Run the installer directly from your project root using `uvx`:

```bash
# Install for Antigravity (.agents/plugins/ by default):
uvx --from git+https://github.com/joshyim/architecture-as-a-code-skills arch-c4 install

# Install for Claude Code (.claude/skills/):
uvx --from git+https://github.com/joshyim/architecture-as-a-code-skills arch-c4 install --target claude

# Install for Cursor / Windsurf (.cursor/rules/ and .cursor/skills/):
uvx --from git+https://github.com/joshyim/architecture-as-a-code-skills arch-c4 install --target cursor

# Install globally across all projects on your machine:
uvx --from git+https://github.com/joshyim/architecture-as-a-code-skills arch-c4 install --global
```

Or install via standard `pip`:

```bash
pip install git+https://github.com/joshyim/architecture-as-a-code-skills
arch-c4 install
```

---

### Option 2: Install as a Git Submodule (Project-Locked)

To lock these skills directly into your repository's version control:

**For Antigravity:**
```bash
git submodule add https://github.com/joshyim/architecture-as-a-code-skills .agents/plugins/architecture-as-code
```
*Antigravity automatically discovers `plugin.json` and loads both skills and rules immediately.*

**For Claude Code:**
```bash
git submodule add https://github.com/joshyim/architecture-as-a-code-skills .claude/skills/architecture-as-code
```

**For Cursor / Windsurf / Other Tools:**
```bash
git submodule add https://github.com/joshyim/architecture-as-a-code-skills tools/architecture-as-code
# Then link or reference rules/c4-dsl-standards.md in your .cursorrules or system instructions.
```

---

## Generated Folder Structure

When `arch-c4-init` runs, it generates the following modular DSL structure:

```
<destination-folder>/
├── README.md               # Architecture documentation & instructions
├── workspace.dsl           # Root workspace aggregating includes
├── models/
│   ├── <name>.dsl          # Software systems, containers, components, external apps
│   ├── <name>_personas.dsl # User roles and personas
│   └── <name>_relations.dsl# Inter-element relationships and communication flows
├── views/
│   └── views.dsl           # Landscape, Context, Container, and Component views
└── styles/
    └── style.dsl           # Color tokens, shapes, and custom tagging styles
```

---

## Recommended `.gitignore` Entries

Structurizr creates runtime cache, layout files, and export images when running locally. Add these to your repo's `.gitignore`:

```gitignore
# Structurizr runtime files
<destination-folder>/.structurizr/
<destination-folder>/images/
<destination-folder>/workspace.json
<destination-folder>/-d
```

---

## Running Structurizr Local with Docker

Structurizr Local lets you view, navigate, and interactively edit your C4 architecture diagrams in the browser. For more details, see the official [Structurizr Local Quickstart](https://docs.structurizr.com/local/quickstart).

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed and running.

---

### Quick Launch via CLI or Helper Script

If you installed via `arch-c4`:
```bash
arch-c4 serve
```

Or using the included helper script:
```bash
./scripts/run-structurizr.sh
```

---

### Manual Launch with Docker

Mount the folder containing your generated `workspace.dsl` into `/usr/local/structurizr` in the container.

Replace `<destination-folder>` with the relative or absolute path where your C4 DSL files are generated (e.g., `docs/architecture` or `structurizr_data`):

```bash
docker run -it --rm -p 8080:8080 \
  -v "$(pwd)/<destination-folder>:/usr/local/structurizr" \
  structurizr/structurizr local
```

**Example** (using `docs/architecture`):

```bash
docker run -it --rm -p 8080:8080 \
  -v "$(pwd)/docs/architecture:/usr/local/structurizr" \
  structurizr/structurizr local
```

---

### Viewing Interactive Diagrams

Once the container is running:

1. Open your browser and navigate to:
   ```
   http://localhost:8080
   ```
2. You will see interactive diagrams including:
   - **System Landscape**: High-level enterprise/ecosystem view
   - **System Context**: Boundaries, users, and external integrations
   - **Container Diagrams**: Deployable units (frontends, backend services, databases)
   - **Component Diagrams**: Internal structural decomposition
3. **Interactive Features**:
   - Double-click containers or systems to drill down into component/container views.
   - Adjust element layout and diagram positions directly in the browser. Layout adjustments are saved locally into your mounted folder.

---

## Validating DSL Files

To validate the syntax of your Structurizr DSL files without starting the web server:

```bash
# Using CLI:
arch-c4 validate

# Or using helper script:
./scripts/validate-dsl.sh

# Or directly via Docker:
docker run --rm \
  -v "$(pwd)/<destination-folder>:/usr/local/structurizr" \
  structurizr/structurizr validate -w workspace.dsl
```
