---
name: odoo-v19-scaffold
description: >
  Scaffold a new Odoo 19 Community Edition development project with Docker.
  Generates docker-compose.yml (Odoo 19.0 + PostgreSQL 16), addons/ folder,
  config/odoo.conf, and .gitignore. Use when a developer wants to start a new
  Odoo 19 custom module project from scratch.
---

# Odoo 19 CE — Project Scaffold

When the developer asks to create, scaffold, or start a new Odoo 19 project,
generate the following files **exactly as shown**. Do not improvise — copy
these templates verbatim.

## Generated Structure

```
project-root/
├── docker-compose.yml
├── config/
│   └── odoo.conf
├── addons/
│   └── .gitkeep
└── .gitignore
```

## 1. docker-compose.yml

Create this file at the project root:

```yaml
services:
  odoo:
    image: odoo:19.0
    depends_on:
      - db
    ports:
      - "8069:8069"
    volumes:
      - odoo-data:/var/lib/odoo
      - ./config:/etc/odoo
      - ./addons:/mnt/extra-addons
    restart: unless-stopped

  db:
    image: postgres:16
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_PASSWORD=odoo
      - POSTGRES_USER=odoo
    volumes:
      - db-data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  odoo-data:
  db-data:
```

## 2. config/odoo.conf

Create `config/` directory and this file inside it:

```ini
[options]
addons_path = /mnt/extra-addons
data_dir = /var/lib/odoo
; admin_passwd = changeme
```

## 3. addons/.gitkeep

Create the `addons/` directory with an empty `.gitkeep` file so git tracks the
empty directory. This is where custom modules go.

## 4. .gitignore

Create this file at the project root:

```gitignore
# Python
__pycache__/
*.py[cod]
*.egg-info/

# Odoo
filestore/
sessions/

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

## After Scaffolding

Tell the developer:

1. Run `docker compose up -d` to start Odoo
2. Open `http://localhost:8069` to access the web interface
3. Create a new database from the database manager
4. Place custom modules in the `addons/` folder
5. Restart Odoo: `docker compose restart odoo`
6. Enable developer mode, then update the apps list to see new modules

**Note:** On first startup with an empty `addons/` folder, Odoo logs a warning
about "invalid addons directory '/mnt/extra-addons'". This is harmless — the
warning disappears once a module is added and Odoo is restarted.
