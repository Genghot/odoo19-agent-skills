## 1. Create Skill File

- [x] 1.1 Create `odoo-v19-scaffold/SKILL.md` with frontmatter (name, description, trigger)
- [x] 1.2 Write the skill instruction section — when to activate, what to generate
- [x] 1.3 Embed docker-compose.yml template as a code block (odoo:19.0, postgres:16, volumes, ports)
- [x] 1.4 Embed config/odoo.conf template as a code block (addons_path, data_dir, admin_passwd)
- [x] 1.5 Embed .gitignore template as a code block (__pycache__, .pyc, IDE dirs, filestore, sessions)
- [x] 1.6 Add instruction for creating addons/ directory with .gitkeep

## 2. Validate

- [x] 2.1 Test: run the skill prompt against the agent, verify all files are generated correctly
- [x] 2.2 Test: run `docker compose up -d` on generated project, confirm Odoo accessible at localhost:8069
- [x] 2.3 Test: place a minimal test module in addons/, update apps list, confirm module is discoverable
- [x] 2.4 Verify .gitignore excludes expected files
