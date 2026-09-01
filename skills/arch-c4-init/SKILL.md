---
name: arch-c4-init
description: Initialize a C4 Structurizr DSL workspace in a new repo through a structured interview, generating all DSL files and .gitignore entries. Use when setting up architecture-as-code for a new project, starting C4 modeling, or adding Structurizr to an existing repo.
compatibility: Requires Docker to run Structurizr Local.
---

# arch-c4-init

Initialize a C4 architecture-as-code workspace (Structurizr DSL) in a target repository by interviewing the user about their system and generating all workspace files ready to run with Structurizr Local.

## Arguments

Look up or ask the user for these inputs:

| Input | Description | Example |
|---|---|---|
| **Destination Folder** | Target directory where C4 workspace files will be created. **Look up parameter `C4_DESTINATION` in the root `.env.dev` file first.** If the entry does not exist, ask the user for the destination. | `docs/architecture` or `structurizr_data` |
| **Project Name** | Short identifier for the system (used in DSL variable names and filenames) | `myapp` |
| **Workspace Title** | Human-readable name for the workspace | `"My App"` |
| **System Description** | One or two sentence description of what the system does | `"A platform for managing..."`|

## Instructions

### Step 1: Look Up Destination & Confirm Inputs

1. **Destination Folder Lookup**:
   - Check the root `.env.dev` file for the parameter `C4_DESTINATION` (e.g., `C4_DESTINATION=structurizr_data` or `C4_DESTINATION=docs/architecture`).
   - If `C4_DESTINATION` exists in `.env.dev`, use its value as the destination folder.
   - If the entry does not exist in `.env.dev` (or `.env.dev` file is missing), ask the user to provide the destination folder.
2. **Confirm Inputs**:
   - Confirm the Destination Folder, Project Name, Workspace Title, and System Description with the user before proceeding. Use `{name}` for the project name in all filenames and DSL identifiers.

### Step 2: Conduct Architecture Interview

Ask the user the following questions. Collect answers in a structured way before proceeding to file generation. You may ask all at once or in logical groups.

#### 2.1 Personas

Ask: *Who are the people that interact with the system? For each, provide a short role name and a one-sentence description.*

Collect 1–6 personas. Example output:
- `end_user` — "Primary user of the application."
- `admin` — "Manages users and configuration."

#### 2.2 External Systems

Ask: *Are there any external software systems your system integrates with? (e.g. payment providers, identity providers, third-party APIs)*

For each external system, collect: name, description. These will be tagged `"external app"`.

#### 2.3 Containers

Ask: *What are the main technical containers (deployable units) that make up your system?*

Collect at minimum:
- **Frontend** — what type? (Web app, mobile app, etc.) and tech stack
- **Backend** — tech stack
- **Datastores** — type and technology (e.g. PostgreSQL, Redis)

#### 2.4 Components (Optional)

Ask: *Within each container, are there high-level functional groups or components you want to model? (Skip if you want to add these later.)*

If provided, collect component name, description, and which container it belongs to. Group related components under a named group if applicable.

#### 2.5 Key Relationships

Ask: *What are the most important interactions? Think: which personas use which frontend features, which frontend calls which backend services, which backend services use which datastores or external systems.*

Collect as a list of: `source -> target "description"`.

### Step 3: Present Summary for Review

Before writing any files, present a structured summary of everything collected:

```
## Architecture Summary: {Workspace Title}

### Personas
- [list]

### Software System: {name}
  Containers:
  - [list with tech]
  Components (if any):
  - [list grouped by container]

### External Systems
- [list]

### Key Relationships
- [list]
```

Ask the user: *Does this look right? Any corrections before I generate the files?*

Iterate until approved.

### Step 4: Generate Files

Once approved, create the following file structure under `{Destination Folder}/` (resolved from `C4_DESTINATION` in root `.env.dev` or provided by user):

#### 4.1 `workspace.dsl`

```dsl
workspace {name} "{Workspace Title}" {

    model {
        !include ./models/{name}.dsl
        !include ./models/{name}_personas.dsl
        !include ./models/{name}_relations.dsl
    }

    views {
        !include ./views/views.dsl

        styles {
            !include ./styles/style.dsl
        }

        properties {
            "structurizr.sort" "type"
        }
    }
}
```

#### 4.2 `models/{name}_personas.dsl`

One `person` element per persona:

```dsl
# {name} personas

{identifier} = person "{Display Name}" {
    description "{description}"
}
```

For personas tagged as future/proposed, add `tags "future"` or `tags "proposed"`.

#### 4.3 `models/{name}.dsl`

The primary software system with all containers and components:

```dsl
# software systems
{name} = softwareSystem "{Workspace Title}" {

    # frontend
    FrontEnd = container "{name} Frontend" {
        technology "{tech}"
        # components here if provided
    }

    # backend
    Backend = container "{name} Backend" {
        description "{description}"
        technology "{tech}"
        # components here, grouped if applicable
    }

    group "Persistent Data" {
        {name}DB = container "{name} DataStore" {
            description "Stores application data."
            technology "{tech}"
        }
    }
}

# External systems
{externalId} = softwareSystem "{External Name}" {
    description "{description}"
    tags "external app"
}
```

Group related components within a container using `group "Group Name" { ... }`.

#### 4.4 `models/{name}_relations.dsl`

All relationships, organized in comment-separated sections:

```dsl
# {name} relationships

## Persona to Frontend
{persona} -> {container} "{description}"

## Frontend to Backend
{frontend} -> {backend} "{description}"

## Backend to DataStore
{backend} -> {datastore} "{description}"

## Backend to External
{backend} -> {external} "{description}"
```

#### 4.5 `views/views.dsl`

Standard views covering landscape, context, container, and component levels:

```dsl
# views
systemLandscape {name} "Landscape" {
    include *
}

systemContext {name} "System_Context" {
    include *
}

container {name} "System_Components" {
    include *
}

component FrontEnd "Frontend_App_Full" {
    include *
}

component Backend "Backend_App_Full" {
    include *
}
```

Add additional `component` views for curated subsets if the user provided focused component groupings.

#### 4.6 `styles/style.dsl`

Standard base styles:

```dsl
# common style definition

element "Person" {
    background #438dd5
    color #ffffff
    fontSize 22
    shape Person
}
element "Software System" {
    background #1168bd
    color #ffffff
}
element "external app" {
    background #999999
}
element "proposed" {
    background #CC5500
    opacity 75
}
element "future" {
    background #7852A9
    opacity 75
}
element "Container" {
    background #438dd5
    color #ffffff
}
element "Web Browser" {
    shape WebBrowser
}
element "Mobile App" {
    shape MobileDeviceLandscape
}
element "Database" {
    shape Cylinder
}
element "Component" {
    background #85bbf0
    color #000000
}
```

#### 4.7 `README.md`

Create `{Destination Folder}/README.md` with:
- Brief description of the system (from the workspace title and system description)
- Folder structure explanation
- Docker commands to run [Structurizr Local](https://docs.structurizr.com/local):

```markdown
# {Workspace Title} — C4 Architecture

{System description}

## Running Structurizr Local

From the repo root:

```bash
docker pull structurizr/structurizr
docker run -it --rm -p 8080:8080 \
  -v "$(pwd)/{Destination Folder}:/usr/local/structurizr" \
  structurizr/structurizr local
```

Then open: http://localhost:8080

## Folder Structure

- `workspace.dsl` — Root workspace; wires together all includes
- `models/` — Software system, containers, components, personas, relationships
- `views/` — View definitions (landscape, context, container, component)
- `styles/` — Visual style definitions
```

#### 4.8 Append `.gitignore`

Append the following to the **repo root** `.gitignore`. If no `.gitignore` exists, create one:

```
# structurizr
{Destination Folder}/.structurizr/
{Destination Folder}/images/
{Destination Folder}/workspace.json
{Destination Folder}/-d
```

### Step 5: Present Completion Summary

After writing all files, present a table:

| File | Action |
|---|---|
| `{Destination Folder}/workspace.dsl` | Created |
| `{Destination Folder}/models/{name}.dsl` | Created |
| `{Destination Folder}/models/{name}_personas.dsl` | Created |
| `{Destination Folder}/models/{name}_relations.dsl` | Created |
| `{Destination Folder}/views/views.dsl` | Created |
| `{Destination Folder}/styles/style.dsl` | Created |
| `{Destination Folder}/README.md` | Created |
| `.gitignore` | Appended |

Then output the docker run command for convenience.

## Notes

- Do NOT write files until the user approves the summary in Step 3
- Use snake_case or camelCase identifiers in DSL consistently (follow what the user uses, default to camelCase)
- Components and relationships are optional at init time — the user can add them later with an update skill
- The `images/` and `.structurizr/` folders are created by Structurizr Local at runtime; do not create them manually
