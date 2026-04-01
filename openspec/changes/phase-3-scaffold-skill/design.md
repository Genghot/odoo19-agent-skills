## Context

We have 3 validated guardrail skills (core, views, sale) that prevent Odoo 19 pitfalls. The next step is real-world adoption. Before developers can use these guardrails, they need a working Odoo 19 dev environment. Today, setting this up means manually assembling docker-compose.yml, odoo.conf, directory structure, and volume mounts — a process that varies across blog posts, tutorials, and Odoo versions.

The scaffold skill is a Claude Code skill (SKILL.md) that instructs the agent to generate a complete, opinionated project structure when a developer asks to start a new Odoo 19 module project.

## Goals / Non-Goals

**Goals:**
- One-prompt setup: developer says "create an Odoo 19 project" and gets a working dev environment
- Docker Compose with Odoo 19.0 CE + PostgreSQL 16, correct volume mounts
- `addons/` directory ready for custom modules
- `config/odoo.conf` with correct `addons_path` including the custom addons mount
- `.gitignore` covering Odoo-specific files (filestore, __pycache__, sessions)
- Best-practice defaults that work immediately with `docker compose up`

**Non-Goals:**
- Enterprise edition support
- Multi-database or production deployment configs
- Nginx/reverse proxy setup
- CI/CD pipeline generation
- Auto-wiring guardrail skills into the generated project (future phase)
- Generating actual module scaffolding (__manifest__.py, models/, views/) — that's a separate skill

## Decisions

### Skill type: generator, not guardrail

The existing skills are guardrails — they prevent mistakes during code generation. This skill is a **generator** — it produces a specific file set. The SKILL.md will contain the exact templates for docker-compose.yml, odoo.conf, and .gitignore so the agent outputs them verbatim rather than improvising.

**Why:** LLMs tend to hallucinate docker-compose syntax or use outdated Odoo image tags. Embedding exact file content in the skill ensures reproducible output.

### Odoo image: `odoo:19.0`

Pin to `odoo:19.0` (Docker Hub official image). Not `latest`, not a specific patch version.

**Why:** `19.0` tracks the latest 19.x patch without breaking on major version changes. The official Docker Hub image is the most accessible for community developers.

### PostgreSQL: `postgres:16`

**Why:** PostgreSQL 16 is the version validated in Phase 2 testing and is the current stable release compatible with Odoo 19.

### Volume strategy: named volumes for data, bind mount for addons

```yaml
volumes:
  - odoo-data:/var/lib/odoo        # filestore, sessions (persist across rebuilds)
  - ./config:/etc/odoo             # odoo.conf
  - ./addons:/mnt/extra-addons     # custom modules (bind mount for live editing)
```

**Why:** Named volumes for data persistence, bind mount for addons so developers see changes immediately. This matches the official Odoo Docker image's expected paths.

### Single SKILL.md with embedded templates

The skill file will contain the exact content of docker-compose.yml, odoo.conf, and .gitignore as code blocks. The agent copies these verbatim when scaffolding.

**Alternative considered:** A skill that references template files in the repo. Rejected because skills must be self-contained — the SKILL.md is the only file the agent reads.

## Risks / Trade-offs

- **[Docker Hub image lag]** → The `odoo:19.0` tag may lag behind git master. Mitigation: this is for development, not production. Developers needing bleeding-edge can build from source.
- **[Opinionated defaults]** → Some developers may want different Postgres versions or port mappings. Mitigation: the scaffold is a starting point, not a constraint. Keeping it simple makes it easy to modify.
- **[No module scaffold]** → This only creates the project shell, not a module. Mitigation: Module scaffolding is a natural follow-up skill. Keeping them separate follows single-responsibility.
