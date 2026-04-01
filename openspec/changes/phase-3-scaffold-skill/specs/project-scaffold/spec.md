## ADDED Requirements

### Requirement: Generate docker-compose.yml
The skill SHALL instruct the agent to create a `docker-compose.yml` at the project root with:
- An `odoo` service using the `odoo:19.0` image
- A `db` service using the `postgres:16` image
- Port mapping `8069:8069` for the web interface
- Named volume `odoo-data` mounted at `/var/lib/odoo`
- Bind mount `./config:/etc/odoo` for configuration
- Bind mount `./addons:/mnt/extra-addons` for custom modules
- Environment variables for PostgreSQL credentials (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`)
- The `odoo` service SHALL depend on `db`
- Restart policy `unless-stopped` for both services

#### Scenario: Developer requests new Odoo project
- **WHEN** a developer asks the agent to create/scaffold a new Odoo 19 project
- **THEN** the agent creates `docker-compose.yml` with all specified services, volumes, and configuration

#### Scenario: Docker Compose starts successfully
- **WHEN** the developer runs `docker compose up -d` in the generated project
- **THEN** Odoo 19 starts and is accessible at `http://localhost:8069`

### Requirement: Generate addons directory
The skill SHALL instruct the agent to create an empty `addons/` directory at the project root with a `.gitkeep` file.

#### Scenario: Addons directory exists after scaffold
- **WHEN** the project is scaffolded
- **THEN** `addons/` directory exists and is tracked by git via `.gitkeep`

### Requirement: Generate odoo.conf
The skill SHALL instruct the agent to create `config/odoo.conf` with:
- `addons_path` including `/mnt/extra-addons`
- `data_dir = /var/lib/odoo`
- `admin_passwd` set to a default value with a comment to change it

#### Scenario: Odoo reads custom addons path
- **WHEN** Odoo starts with the generated config
- **THEN** modules in `addons/` are discoverable via Apps menu (after enabling developer mode and updating apps list)

### Requirement: Generate .gitignore
The skill SHALL instruct the agent to create a `.gitignore` covering:
- `__pycache__/`
- `*.pyc`
- `.idea/` and `.vscode/` (IDE directories)
- `filestore/`
- `sessions/`

#### Scenario: Python bytecode not tracked
- **WHEN** the developer runs Odoo and Python generates `.pyc` files
- **THEN** those files are excluded from git tracking

### Requirement: Skill is self-contained
The SKILL.md file SHALL contain the complete content of all generated files as embedded code blocks. The agent SHALL copy these verbatim, not generate them from memory.

#### Scenario: Reproducible output
- **WHEN** two different agents process the same scaffold request using this skill
- **THEN** both produce identical docker-compose.yml, odoo.conf, and .gitignore content
