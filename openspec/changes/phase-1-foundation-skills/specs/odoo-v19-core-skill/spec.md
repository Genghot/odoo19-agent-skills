## ADDED Requirements

### Requirement: Core SKILL.md with smart description
The skill SHALL have a SKILL.md file with YAML frontmatter containing `name: odoo-v19-core`, a description that includes keywords: ORM, field types, model inheritance, `_inherit`, `_inherits`, `api.depends`, `api.onchange`, `api.constrains`, `api.model`, security, `ir.model.access`, `ir.rule`, controllers, wizards, `__manifest__.py`, module structure. The description SHALL be under 1024 characters.

#### Scenario: Agent activates on ORM query
- **WHEN** a user asks "how do I add a computed field to my model?"
- **THEN** the agent matches the description keywords and loads the odoo-v19-core skill

#### Scenario: Agent activates on security query
- **WHEN** a user asks "set up access control for my custom model"
- **THEN** the agent matches "security", "ir.model.access", "ir.rule" in the description and loads the skill

### Requirement: Business Context section
The SKILL.md body SHALL begin with a Business Context section explaining that this skill covers the Odoo 19 core framework used by all modules — the ORM, field system, inheritance mechanisms, security layer, web controllers, and transient model wizards.

#### Scenario: Agent reads business context
- **WHEN** the skill is activated
- **THEN** the agent immediately understands this is the foundational framework skill applicable to any Odoo development task

### Requirement: Key Models & Relations section
The SKILL.md SHALL include a Key Models & Relations section covering: `models.Model`, `models.TransientModel`, `models.AbstractModel`, field types (Char, Integer, Float, Boolean, Date, Datetime, Selection, Many2one, One2many, Many2many, Html, Binary, Monetary, Reference), and the `api` decorators (`depends`, `onchange`, `constrains`, `model`, `model_create_multi`).

#### Scenario: Developer looks up field types
- **WHEN** the agent needs to declare a field
- **THEN** the Key Models section provides the correct field class and common parameters (string, required, default, compute, inverse, store, related)

### Requirement: Inheritance patterns documentation
The SKILL.md SHALL document three inheritance mechanisms: classical inheritance (`_inherit` without `_name`), prototype inheritance (`_inherit` with new `_name`), and delegation inheritance (`_inherits`), with a concise code example for each.

#### Scenario: Developer extends an existing model
- **WHEN** user asks "add a field to res.partner"
- **THEN** the skill shows the `_inherit = 'res.partner'` pattern with a field declaration example

### Requirement: Security patterns documentation
The SKILL.md SHALL document access control lists (`ir.model.access.csv` format) and record rules (`ir.rule` XML format), including the column meanings and a minimal example of each.

#### Scenario: Developer sets up access rights
- **WHEN** user asks "create security for my custom model"
- **THEN** the skill provides the CSV header format and an XML record rule example

### Requirement: Extension Patterns section
The SKILL.md SHALL include an Extension Patterns section covering: adding fields to existing models, overriding methods with `super()`, extending views with XPath (reference to odoo-v19-views), and adding menu items.

#### Scenario: Developer customizes Odoo behavior
- **WHEN** user asks "override the create method on sale.order"
- **THEN** the skill shows the `def create(self, vals_list)` override pattern with `super()` call

### Requirement: Common Pitfalls section
The SKILL.md SHALL include at least 5 common pitfalls, including: forgetting `super()` in overrides, missing `store=True` on computed fields that need DB queries/grouping, using `@api.onchange` for stored fields (should use compute), security CSV column order mistakes, and not adding fields to `__init__.py` imports.

#### Scenario: Agent avoids common mistakes
- **WHEN** the agent writes a computed field
- **THEN** it knows to include `store=True` if the field will be used in search/group-by, because the pitfalls section warns about this

### Requirement: Reference files for deep content
The skill SHALL include reference files: `references/field-types.md` (all field types with parameters), `references/inheritance-patterns.md` (detailed examples), `references/security-acl.md` (full ACL and record rule patterns), `references/controllers-routes.md` (HTTP controller patterns), `references/module-scaffold.md` (complete module directory structure with file templates).

#### Scenario: Agent needs detailed field parameters
- **WHEN** the agent needs to know all parameters for a Many2many field
- **THEN** it reads `references/field-types.md` which lists the field class with all supported parameters

### Requirement: Token budget compliance
The SKILL.md body SHALL be under 5000 tokens (~400 lines). Each reference file SHALL be under 3000 tokens (~250 lines).

#### Scenario: Skill fits context budget
- **WHEN** the agent activates the skill
- **THEN** the SKILL.md loads within the 5K token budget, leaving room for other skills and conversation context
