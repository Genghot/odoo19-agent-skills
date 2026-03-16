## ADDED Requirements

### Requirement: Views SKILL.md with smart description
The skill SHALL have a SKILL.md file with YAML frontmatter containing `name: odoo-v19-views`, a description that includes keywords: QWeb, form view, list view, tree view, kanban view, search view, XPath, `ir.actions.act_window`, `ir.ui.menu`, XML views, view inheritance, `position="after"`, `position="inside"`, `position="replace"`, `position="attributes"`. The description SHALL be under 1024 characters.

#### Scenario: Agent activates on view modification query
- **WHEN** a user asks "add a field to the sale order form view"
- **THEN** the agent matches "form view", "XPath", "view inheritance" and loads the odoo-v19-views skill

#### Scenario: Agent activates on menu query
- **WHEN** a user asks "create a menu item for my custom model"
- **THEN** the agent matches "ir.ui.menu", "ir.actions.act_window" and loads the skill

### Requirement: Business Context section
The SKILL.md body SHALL explain that Odoo views are defined in XML data files, use QWeb templating for kanban/website views, and are inherited via XPath expressions. It SHALL note that views are loaded from the `views/` directory and declared in `__manifest__.py`.

#### Scenario: Agent understands view system
- **WHEN** the skill is activated
- **THEN** the agent knows views are XML-based, loaded via manifest, and extended through inheritance

### Requirement: Form view documentation
The SKILL.md SHALL document form view structure including: `<form>`, `<sheet>`, `<group>`, `<notebook>`/`<page>`, `<header>` (for status bar and buttons), button types (action, object), `<field>` attributes (widget, invisible, readonly, required, domain), and the `statusbar` widget pattern.

#### Scenario: Developer creates a form view
- **WHEN** user asks "create a form view for my model"
- **THEN** the skill provides the standard form view skeleton with sheet, header, groups, and notebook

### Requirement: List and kanban view documentation
The SKILL.md SHALL document list view (`<list>`) with key attributes (editable, multi_edit, decoration-*) and kanban view (`<kanban>`) with QWeb template structure (`<templates>`, `<t t-name="card">`), field declarations, and color/decoration patterns.

#### Scenario: Developer creates a kanban view
- **WHEN** user asks "add a kanban view"
- **THEN** the skill shows the kanban XML structure with the QWeb template pattern

### Requirement: Search view and filters documentation
The SKILL.md SHALL document search view (`<search>`) with `<field>` (for autocomplete search), `<filter>` (with domain and date grouping), `<group>` (for group-by), and default filter activation via action context.

#### Scenario: Developer adds search filters
- **WHEN** user asks "add a date filter to the list view"
- **THEN** the skill shows the search view filter pattern with domain syntax

### Requirement: XPath inheritance patterns
The SKILL.md SHALL document view inheritance with `<xpath expr="..." position="...">` covering all position values: `inside`, `after`, `before`, `replace`, `attributes`. It SHALL include the `inherit_id` reference pattern and at least 2 concise XPath examples.

#### Scenario: Developer extends an existing view
- **WHEN** user asks "add a field after the partner_id in the sale order form"
- **THEN** the skill shows the XPath pattern: `<xpath expr="//field[@name='partner_id']" position="after">`

### Requirement: Actions and menus documentation
The SKILL.md SHALL document `ir.actions.act_window` (with view_mode, res_model, domain, context) and `ir.ui.menu` (with parent, action, sequence). It SHALL show how to link a menu to an action.

#### Scenario: Developer creates navigation
- **WHEN** user asks "add a menu item for my model"
- **THEN** the skill provides the action + menu XML pattern

### Requirement: Common Pitfalls section
The SKILL.md SHALL include at least 4 pitfalls: XPath expressions that don't match (field name typos, wrong parent element), forgetting `inherit_id` ref, using `tree` vs `list` tag (v19 uses `<list>`), and `invisible`/`readonly` domain syntax changes in v19 (Python expression strings, not list-of-tuples).

#### Scenario: Agent avoids XPath mistakes
- **WHEN** the agent writes an XPath expression
- **THEN** it knows to verify the target field/element exists in the parent view because the pitfalls section warns about non-matching expressions

### Requirement: Reference files for deep content
The skill SHALL include reference files: `references/form-view.md` (complete form view elements and attributes), `references/list-view.md` (list view attributes and features), `references/kanban-view.md` (kanban QWeb patterns), `references/search-view.md` (search view patterns), `references/xpath-patterns.md` (comprehensive XPath examples for common extension scenarios).

#### Scenario: Agent needs detailed widget list
- **WHEN** the agent needs to know available field widgets
- **THEN** it reads `references/form-view.md` which lists common widgets and their use cases

### Requirement: Token budget compliance
The SKILL.md body SHALL be under 5000 tokens (~400 lines). Each reference file SHALL be under 3000 tokens (~250 lines).

#### Scenario: Skill fits context budget
- **WHEN** the agent activates the skill
- **THEN** the SKILL.md loads within the 5K token budget
