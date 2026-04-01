## Why

Starting an Odoo 19 custom module project requires getting Docker, PostgreSQL, addons paths, and config right before writing any module code. Developers waste time on boilerplate setup and hit configuration issues (wrong image tags, missing volume mounts, incorrect addons paths). A scaffold skill eliminates this friction — one prompt creates a ready-to-develop project.

This is also the first step toward real-world distribution: a developer installs the scaffold skill, gets a working project, and the guardrail skills (core/views/sale) are already wired in.

## What Changes

- New **scaffold skill** (`odoo-v19-scaffold`) that generates a complete project structure:
  - `docker-compose.yml` — Odoo 19.0 CE + PostgreSQL 16, correct volume mounts
  - `addons/` — empty directory for custom modules
  - `config/odoo.conf` — pre-configured with correct addons path
  - `.gitignore` — Odoo-appropriate ignores (filestore, sessions, __pycache__)
- The skill acts as a **generator** (produces files) rather than a pure guardrail (prevents mistakes)
- Includes best-practice defaults: persistent filestore, web port mapping, restart policy

## Capabilities

### New Capabilities
- `project-scaffold`: Generate a complete Odoo 19 CE development project with Docker Compose, addons folder, and configuration ready for custom module development

### Modified Capabilities

_None — existing guardrail skills are unchanged._

## Impact

- New skill file: `odoo-v19-scaffold/SKILL.md`
- No changes to existing guardrail skills
- Consumer projects can use this as their entry point, then add guardrail skills for development
