# Odoo 19 Pitfall Catalog

> Source of truth for all v19 breaking changes and wrong patterns discovered through failure-driven testing.
> Each entry is backed by a real Docker install failure or code review finding.

---

## HARD_FAIL — Install Crashes

### HF-01: `category_id` removed from `res.groups`

- **Domain**: core / security
- **Error**: `ValueError: Invalid field 'category_id' in 'res.groups'`
- **Wrong**:
  ```xml
  <record id="group_foo" model="res.groups">
      <field name="category_id" ref="base.module_category_sales"/>
  </record>
  ```
- **Correct**: Remove `category_id` line entirely. Groups no longer belong to module categories in v19.
  ```xml
  <record id="group_foo" model="res.groups">
      <field name="name">Foo Group</field>
      <field name="implied_ids" eval="[(4, ref('other.group'))]"/>
  </record>
  ```
- **Triggered by**: core/03-security-groups-acl, Phase 1 Test 5
- **Consistency**: Reproduced in 3/3 runs

### HF-02: `project.milestone` model name collision

- **Domain**: core / model naming
- **Error**: `ValueError: Wrong @depends on '_compute_milestone_reached_count'... Dependency field 'is_reached' not found`
- **Wrong**: Using `_name = 'project.milestone'` — this model already exists in Odoo 19's `project` module
- **Correct**: Check if a model name exists before using it. Use a prefixed name like `_name = 'project.custom.milestone'` or `_name = 'x_project_milestone'`
- **Triggered by**: views/01-form-list-view
- **Consistency**: 3/3 runs (deterministic — model always exists in project module)
- **Note**: This is not just `project.milestone` — many standard model names are taken. The model should verify.

### HF-03: `expand` attribute on `<group>` in search view

- **Domain**: views / search
- **Error**: `RELAXNG_ERR_INVALIDATTR: Invalid attribute expand for element group`
- **Wrong**:
  ```xml
  <group expand="0" string="Group By">
  ```
- **Correct**: `<group>` in search views does not support `expand` in v19. Just use:
  ```xml
  <group>
  ```
- **Triggered by**: views/03-search-view-filters
- **Consistency**: 3/3 runs

### HF-04: `string` attribute on `<group>` in search view

- **Domain**: views / search
- **Error**: `RELAXNG_ERR_INVALIDATTR: Invalid attribute string for element group`
- **Wrong**:
  ```xml
  <group string="Group By">
  ```
- **Correct**: `<group>` in search views does not support `string` in v19. Just use:
  ```xml
  <group>
  ```
- **Triggered by**: views/03-search-view-filters
- **Consistency**: 3/3 runs (same module as HF-03)

### HF-05: `base.view_partner_list` external ID doesn't exist

- **Domain**: views / XPath inheritance
- **Error**: `ValueError: External ID not found in the system: base.view_partner_list`
- **Wrong**:
  ```xml
  <field name="inherit_id" ref="base.view_partner_list"/>
  ```
- **Correct**: The partner list view XML ID is `base.view_partner_tree` (historical name kept):
  ```xml
  <field name="inherit_id" ref="base.view_partner_tree"/>
  ```
- **Triggered by**: views/04-xpath-inheritance
- **Consistency**: 3/3 runs
- **Note**: Despite Odoo 19 using `<list>` tag in XML, many view external IDs still use `_tree` suffix

---

## WRONG_PATTERN — Installs but Incorrect

### WP-01: `name_get()` override instead of `_compute_display_name`

- **Domain**: core / ORM
- **Wrong**:
  ```python
  def name_get(self):
      return [(rec.id, f"{rec.name} [{rec.level}]") for rec in self]
  ```
- **Correct**: `name_get` was deprecated in v17. Use `_compute_display_name`:
  ```python
  def _compute_display_name(self):
      for rec in self:
          rec.display_name = f"{rec.name} [{rec.level}]"
  ```
- **Triggered by**: core/02-model-inheritance
- **Consistency**: 2/3 runs

### WP-02: Record rules missing `noupdate="1"`

- **Domain**: core / security
- **Wrong**: Record rules defined without `<data noupdate="1">` wrapper
- **Correct**: Always wrap record rules in `<data noupdate="1">` to prevent overwrite on module upgrade:
  ```xml
  <data noupdate="1">
      <record id="rule_foo" model="ir.rule">...</record>
  </data>
  ```
- **Triggered by**: core/03-security-groups-acl
- **Consistency**: 2/3 runs

---

## Findings from Phase 1 (Previously Discovered)

### HF-P1: Settings form XPath `//app[@name='general']` doesn't exist

- **Domain**: views / settings
- **Error**: `Element '<xpath expr="//app[@name='general']">' cannot be located in parent view`
- **Wrong**: `<xpath expr="//app[@name='general']" position="inside">`
- **Correct**: The settings form structure changed in v19 CE. Need to target a valid element that exists in `base.res_config_settings_view_form`.
- **Triggered by**: Phase 1 Test 1 (sale_discount_approval), views/05-settings-config-view
- **Note**: equipment_settings module passed because it used a different XPath approach — worth investigating which approach works

---

## Statistics

| Category | Count |
|----------|-------|
| HARD_FAIL | 5 (+ 1 from Phase 1) |
| WRONG_PATTERN | 2 |
| Total pitfalls | 7 (+ 1) |
| Modules tested | 15 |
| First-attempt install success | 10/15 (67%) |
| After fixes | 15/15 (100%) |
