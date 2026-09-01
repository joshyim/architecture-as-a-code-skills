# Architecture Synchronization Rule (Pre-Commit, Review & PR Gate)

Enforce architecture-as-code synchronization whenever code changes are completed, tested, and prepared for commit, review, or Pull Request (PR) generation:

## Trigger Conditions
This rule applies when:
- **Ready for Review & Testing**: A set of work or feature implementation is complete and ready for code review, verification, or unit testing.
- **Pre-Commit / Check-In**: Code changes are about to be staged, committed, or checked into git.
- **PR Generation / Creation**: A Pull Request (PR) is being prepared, drafted, or generated (e.g., summarizing changes or running `gh pr create`).
- **Architectural Scope**: The changes add, remove, or modify any container, service, worker, database, external third-party API integration, or user persona.

## Required Actions

1. **Check for Existing Architecture Workspace**:
   - Inspect `.env.dev` for `C4_DESTINATION` (e.g., `C4_DESTINATION=docs/architecture`).
   - If not found in `.env.dev`, search the repository for `workspace.dsl`.

2. **Synchronize Architecture Diagrams**:
   - **If no C4 workspace exists**:
     - Check if the project warrants a C4 model. If new architectural services/containers were created, trigger the `arch-c4-init` skill to initialize the architecture baseline.
   - **If a C4 workspace already exists**:
     - Trigger the `arch-c4-update` skill to incorporate:
       - New or modified containers / deployable units (frontend, backend services, microservices).
       - New datastores, caches, or message brokers.
       - New external systems, payment gateways, or third-party APIs.
       - New user roles or personas.
       - Updated communication flows and inter-service relationships.

3. **Validate and Bundle in Commit / PR**:
   - Validate DSL syntax using `arch-c4 validate` or `./scripts/validate-dsl.sh`.
   - **Include the updated C4 files in the same commit and PR** as the feature code so code reviewers can review the architecture diff alongside the implementation.
