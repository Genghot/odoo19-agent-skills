# Odoo 19 Agent Skills

Agent skills for Odoo 19 Community Edition development. These skills plug into Claude Code (or any agent that reads SKILL.md files) to prevent common pitfalls and scaffold projects.

## Skills

| Skill | Type | Description |
|-------|------|-------------|
| `odoo-v19-scaffold` | Generator | Scaffold a new Odoo 19 CE project (docker-compose, addons, config) |
| `odoo-v19-core-guard` | Guardrail | Prevent ORM, security, and module structure pitfalls |
| `odoo-v19-views-guard` | Guardrail | Prevent view inheritance, XPath, and UI pitfalls |
| `odoo-v19-sale-guard` | Guardrail | Prevent sale order, quotation, and invoicing pitfalls |

## Quick Start

### Option 1: Git submodule (recommended)

```bash
cd your-odoo-project
git submodule add https://github.com/Genghot/odoo19-agent-skills.git .skills/odoo19-agent-skills
```

Then symlink skills into your agent's skill directory:

```bash
# Claude Code
mkdir -p .claude/skills
ln -s ../../.skills/odoo19-agent-skills/odoo-v19-scaffold .claude/skills/
ln -s ../../.skills/odoo19-agent-skills/odoo-v19-core-guard .claude/skills/
ln -s ../../.skills/odoo19-agent-skills/odoo-v19-views-guard .claude/skills/
ln -s ../../.skills/odoo19-agent-skills/odoo-v19-sale-guard .claude/skills/
```

### Option 2: Copy individual skills

Copy the `SKILL.md` file from any skill directory into your agent's skill folder.

## Initialize a New Odoo 19 Project

Once skills are installed, ask your agent to scaffold the project:

```
> Create a new Odoo 19 project for my custom module
```

The agent generates a ready-to-run project:

```
my-odoo-project/
├── docker-compose.yml    # Odoo 19.0 + PostgreSQL 16
├── config/
│   └── odoo.conf         # Pre-configured addons path
├── addons/
│   └── .gitkeep          # Your custom modules go here
└── .gitignore
```

Then start developing:

```bash
# 1. Start the environment
docker compose up -d

# 2. Open Odoo
open http://localhost:8069

# 3. Create a database from the database manager

# 4. Ask the agent to create your module
#    The guardrail skills automatically prevent v19 pitfalls
> Create a custom module called inventory_barcode in the addons folder

# 5. Restart Odoo and update apps list
docker compose restart odoo
```

The guardrail skills (`core-guard`, `views-guard`, `sale-guard`) activate automatically during module development, preventing known Odoo 19 breaking changes as the agent writes code.

## What the Guardrails Prevent

Tested against 15 prompts on Odoo 19.0 CE with Docker:

| Metric | Without Skills | With Skills |
|--------|---------------|-------------|
| First-attempt install | 67% | 93% |
| Known pitfalls hit | 7 | 0 |

### Pitfalls Covered

- **HF-01**: `category_id` removed from `res.groups` (crashes install)
- **HF-02**: Model name collisions with standard Odoo models
- **HF-03**: `expand` attribute on search `<group>` (invalid in v19)
- **HF-04**: `string` attribute on search `<group>` (invalid in v19)
- **HF-05**: Wrong view XML IDs (`base.view_partner_list` vs `base.view_partner_tree`)
- **HF-P1**: Settings view XPath `//app[@name='general']` (removed in v19)
- **WP-01**: `name_get()` deprecated, use `_compute_display_name`
- **WP-02**: Record rules missing `noupdate="1"` wrapper

## Project Structure

```
odoo-v19-scaffold/SKILL.md       # Project scaffold skill
odoo-v19-core-guard/SKILL.md     # Core framework guardrails
odoo-v19-views-guard/SKILL.md    # View/UI guardrails
odoo-v19-sale-guard/SKILL.md     # Sale module guardrails
documents/                        # Test results and research
archive/                          # Superseded Phase 1 skills
```

## License

LGPL-3
