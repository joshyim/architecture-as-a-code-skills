---
name: fn-domain-discovery
description: Analyzes database schemas, migration epics, foreign key topologies, and application code outlines using cocoindex-code (ccc) to systematically discover and partition cohesive architectural domains and bounded contexts for system modeling and ER diagrams.
compatibility: Compatible with any codebase indexed by cocoindex-code (ccc) and standard RDBMS/ORM configurations.
---

# fn-domain-discovery

Systematically discovers, partitions, and aligns architectural **domains and bounded contexts** across a software system. 

This skill bridges the gap between database schemas and application code. It analyzes database migration history, foreign key graph topologies, and **semantic code outlines via `cocoindex-code` (`ccc`)** to determine cohesive domain boundaries, preventing information overload in architecture diagrams, documentation, and data models.

---

## When to Use This Skill

- When decomposing a monolithic or multi-table database schema into modular, domain-specific ER diagrams (e.g., in [`arch-db-diagram-init`](../arch-db-diagram-init/SKILL.md)).
- When designing or updating C4 container and component boundaries (e.g., in [`arch-c4-init`](../arch-c4-init/SKILL.md) or [`arch-c4-update`](../arch-c4-update/SKILL.md)).
- When identifying bounded contexts, service boundaries, or modular package structures in an existing codebase.

---

## The 5-Pillar Domain Discovery Framework

A domain is **not** determined arbitrarily or by table name alone. It is derived through 5 converging pillars:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   5-PILLAR DOMAIN DISCOVERY FRAMEWORK                  │
├─────────────────────────┬─────────────────────────┬────────────────────┤
│ 1. Schema Topology      │ 2. Migration Epics      │ 3. Code Outlines   │
│    - FK Dependency Tree │    - Migration sequence │    - ccc search    │
│    - CASCADE lifecycles │    - Commit rationale   │    - Route groups  │
│    - Junction mappings  │    - Business features  │    - Service layers│
├─────────────────────────┴─────────────────────────┴────────────────────┤
│ 4. Domain-Driven Bounded Contexts (Aggregates & Ubiquitous Language)   │
├────────────────────────────────────────────────────────────────────────┤
│ 5. Cognitive Load Optimization (Miller's Law: 3–6 tables per domain)   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## Step-by-Step Instructions

### Step 1: Discover Table Inventory & FK Topology

First, conduct a static read of all database tables, columns, and foreign key constraints:

1. **Scan Migration Directory or DDL Files:**
   - Locate migration folders (e.g., `backend/sql/`, `migrations/`, `alembic/`, `prisma/`).
   - Extract table names, foreign keys (`REFERENCES table(id)`), and cascading rules (`ON DELETE CASCADE`, `ON DELETE SET NULL`).
2. **Build the Foreign Key Dependency Graph:**
   - **Strong Ownership (Parent-Child):** Tables linked via `ON DELETE CASCADE` belong to the same aggregate/domain (e.g., `runs` → `records` → `assignments`).
   - **Junction Tables:** Tables implementing many-to-many relationships belong to the domain that manages the relationship lifecycle.
   - **Weak / Cross-Domain References:** Tables linked via `ON DELETE SET NULL` or nullable foreign keys typically signal a **cross-domain integration boundary** (e.g., a trace referencing an API key or an organization).

---

### Step 2: Trace Chronological Migration Epics

Examine how the schema evolved over time. Schema migrations reveal the feature epics and business intents behind groups of tables:

1. **Read Migration Filenames and Comments in Sequence:**
   - Initial core tables (`001_eval_tasks.sql`, `002_execution_engine.sql`) indicate the foundational domain.
   - Registration and security migrations (`005_application_registration.sql`) indicate an identity or multi-tenancy domain.
   - Specialized feature migrations (`009_embeddings_and_clusters.sql`) indicate dedicated analytical or machine learning extensions.
   - Curation and labeling migrations (`010_candidate_sets.sql`, `011_cluster_labels.sql`) indicate workflow and user curation domains.
2. **Note Epic Groupings:**
   Group tables that were added or altered together to deliver a single product capability.

---

### Step 3: Analyze Code Outlines using `cocoindex-code` (`ccc`)

Ground the database tables in actual application code by inspecting the code outline and semantic chunks indexed by `cocoindex-code`.

> [!TIP]
> **Using `ccc` for Code Outline Discovery:**
> Run semantic queries using `ccc search` to discover which API routes, service classes, and data access layers operate on which tables.

#### 3.1 Inspect API Routing Outlines
Determine how controllers, HTTP route handlers, and URL prefixes group business operations:
```bash
ccc search "router endpoints route handlers APIRouter"
```
Or filter by route path:
```bash
ccc search --path '*/api/*' "route registration endpoint handlers"
```
*Look for:* Route prefixes such as `/api/v1/auth`, `/api/v1/telemetry`, `/api/v1/clusters`, `/api/v1/candidate-sets`. Tables served by the same router group strongly belong to that functional domain.

#### 3.2 Inspect Service & Business Logic Outlines
Identify which service classes, background workers, or engines encapsulate operations on candidate tables:
```bash
ccc search "<table_name> service business logic processing"
```
*Examples:*
```bash
ccc search "clustering runs cluster records fastcluster Ward"
ccc search "api_keys organizations authenticate verify token"
ccc search "spans traces ingestion otlp protobuf parser"
```
*Look for:* Methods and classes that import or manipulate multiple tables simultaneously. If Class `A` coordinates tables `X`, `Y`, and `Z` within a single transaction, `X`, `Y`, and `Z` form a cohesive domain.

#### 3.3 Inspect Query & Database Client Patterns
Discover which tables are joined together in actual SQL queries or ORM models:
```bash
ccc search "SELECT FROM <table_name> JOIN"
```
*Look for:* High-frequency joins. Tables that are regularly joined in analytical or transactional queries belong together; tables connected only through loose lookup IDs belong in separate domains.

#### 3.4 Inspect Data Transfer Objects (DTOs) & Pydantic/ORM Models
Identify model boundaries in Python, TypeScript, or Go:
```bash
ccc search --path '*/models*' "class BaseModel schema"
```
*Look for:* Nested schemas where one model contains lists of another model (e.g., `ClusterResponse` containing `List[ClusterRecord]`).

---

### Step 4: Synthesize the Domain Matrix

Synthesize the findings from Steps 1–3 into a structured Domain Mapping Matrix:

| Domain Name | Primary Tables | Code Outline / Service Layer | API Router / Endpoints | Rationale & Lifecycle Coupling |
|:---|:---|:---|:---|:---|
| **Identity & Access Management** | `organizations`, `api_keys`, `services` | `auth.py`, `org_service.py` | `/api/v1/orgs`, `/api/v1/keys` | Auth boundary, API token verification, tenant scoping. |
| **Telemetry & Observability** | `traces`, `spans`, `tasks`, `eval_runs` | `telemetry_service.py`, `otlp.py` | `/api/v1/telemetry`, `/api/v1/traces` | High-throughput ingestion, OTel trace spans, execution logs. |
| **Vector Embeddings & Clustering** | `concept_embeddings`, `clustering_runs`, `cluster_records`, `cluster_trace_assignments` | `clustering_engine.py`, `embedding_service.py` | `/api/v1/clusters` | Vector representations, Ward hierarchical clustering, UMAP projections. |
| **Candidate Sets & Semantics** | `candidate_sets`, `candidate_set_traces`, `cluster_labels`, `cluster_keyword_tags` | `candidate_service.py`, `labeling.py` | `/api/v1/candidate-sets` | Human-in-the-loop test curation, LLM topic labels, keyword tags. |
| **Operations & Migrations** | `schema_migrations` | `apply_migration.py` | CLI / Infra scripts | DDL migration ledger, version tracking. |

---

### Step 5: Apply Cognitive Load Optimization (Miller's Law)

Verify that the resulting domain partition is clean, readable, and human-friendly:

1. **Domain Count:** Ensure total domains are between **3 and 6**. (More than 6 leads to fragmentation; fewer than 3 leads to monolithic overload).
2. **Table Density:** Ensure each domain contains between **2 and 6 tables**.
3. **Cross-Domain Reference Check:**
   - Relationships *within* a domain should be dense (parent-child, cascade delete).
   - Relationships *between* domains should be sparse (typically scoping foreign keys like `org_id` or logical reference IDs).

---

### Step 6: Present Domain Proposal for Alignment

Before generating architecture diagrams or restructuring code, present the discovered domains to the user in a clear summary:

```markdown
### Proposed Domain Breakdown

1. **{Domain 1 Name}**
   - **Tables:** `table_a`, `table_b`
   - **Service Boundary:** `service_a.py`, `/api/v1/endpoint_a`
   - **Coupling:** Parent-child cascade, shared transaction boundary.

2. **{Domain 2 Name}**
   ...

Does this partitioning accurately represent your system's architecture before we generate the diagrams?
```

Once confirmed, feed the resulting domain structure directly into [`arch-db-diagram-init`](../arch-db-diagram-init/SKILL.md) to generate the modular `.mmd` diagrams and `overview.md`.
