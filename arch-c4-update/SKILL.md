---
name: arch-c4-update
description: Update an existing C4 architecture diagram in Structurizr DSL. Use when refreshing existing workspace.dsl, models, relationships, views, styles, or README files from the current codebase, including adding containers, components, deployment flows, manual layout-ready views, or validation for stale DSL references.
compatibility: Requires Docker to view and edit diagrams with Structurizr Local; DSL validation can use the Structurizr validate command.
---

# arch-c4-update

Update an existing C4 architecture-as-code workspace (Structurizr DSL). Use this
for maintenance and refresh work. Use `arch-c4-init` instead when no C4 workspace
exists yet and one needs to be created from scratch.

## Core Workflow

1. Find the existing workspace.
   - Look up parameter `C4_DESTINATION` in the root `.env.dev` file.
   - If `C4_DESTINATION` exists in `.env.dev`, look for `workspace.dsl` within that destination folder.
   - If the entry does not exist in `.env.dev` (or `.env.dev` is missing):
     - Ask the user for the destination folder path.
     - Fall back to searching likely repo locations such as `structurizr_data/`, `structurizr/`, or files named `workspace.dsl`.
   - Read `workspace.dsl` first to learn included model, view, and style files.

2. Read the current DSL before planning edits.
   - Inspect `models/*.dsl`, especially software systems, personas, and relations.
   - Inspect `views/*.dsl` to understand current view keys and include scopes.
   - Inspect `styles/*.dsl` and any architecture README/docs.
   - Preserve stable identifiers where practical; changing identifiers can break
     relationships, views, layout metadata, and external references.

3. Use codemaps before live code.
   - Look for repo-local repomix skills such as
     `.agents/skills/repomix-reference-*`.
   - Start with `references/project-structure.md` for shape and entrypoints.
   - Then read `references/tech-stacks.md` for languages, frameworks, and deps.
   - Use targeted searches in `references/files.md` for routes, services, config,
     schemas, deployment scripts, and integration names.
   - Read live source files only when codemaps are missing, stale, ambiguous, or
     not detailed enough for the diagram update.

4. Clarify only product-level choices.
   - Ask when the user must choose scope, audience, diagram depth, deployment
     inclusion, or whether to move/rename the C4 workspace.
   - Do not ask questions that can be answered from the DSL, codemaps, or code.

5. Update the DSL as a coherent set.
   - Update model elements for actual people, containers, components, datastores,
     and external systems.
   - Update relationships at the same time as elements so no stale references
     remain.
   - Update views to include the refreshed elements and create focused views for
     important flows such as ingestion, retrieval, deployment, auth, or data.
   - Do not add `autoLayout` by default; leave views in manual layout mode unless
     the user explicitly requests automatic layout.
   - Update styles only for tags that are actually used.
   - Update README/docs when scope, view list, or run instructions change.

6. Keep the diagram bounded.
   - Model only the repo areas and runtime concerns the user requested.
   - Avoid adding unrelated infrastructure, speculative future components, or
     implementation details that do not help the architecture view.
   - Prefer behavior-level component names over file-by-file inventories.

## Structurizr DSL Guidelines

- Keep identifiers consistent with the existing workspace style, usually
  camelCase unless the workspace already uses another convention.
- Prefer modifying existing elements over deleting and recreating them.
- Use groups sparingly for meaningful architecture clusters.
- Component views should show a useful slice, not every possible relationship.
- `autoLayout tb` is the Structurizr way to force top-to-bottom automatic layout,
  but it keeps the view in automatic layout mode. Do not use it when the user
  wants manual control.
- If deployment details are included, distinguish hosting, identity, secret
  stores, databases, and third-party services with tags and styles.
- Treat generated runtime folders such as `.structurizr/`, `images/`, and
  `workspace.json` as outputs, not source files to edit.

## Validation

After edits:

- Run `git diff --check`.
- Search the C4 workspace for removed or renamed identifiers that should no
  longer appear.
- Check that every view includes only existing elements.
- Check that every relationship source and target exists.
- If available, validate with the Structurizr `validate` command and view or
  edit diagrams with [Structurizr Local](https://docs.structurizr.com/local).
- If Docker or the Structurizr commands are unavailable, say so clearly and
  report the static checks that did run.

## Completion Summary

Report:

- Files changed.
- Architecture areas updated.
- Validation performed and any validation gaps.
- Any assumptions about scope or code freshness.
