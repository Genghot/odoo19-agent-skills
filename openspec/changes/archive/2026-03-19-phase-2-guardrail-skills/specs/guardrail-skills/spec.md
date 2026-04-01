## ADDED Requirements

### Requirement: Guardrail skill structure
Each guardrail skill MUST be a single `SKILL.md` file in its own directory (`odoo-v19-{domain}-guard/SKILL.md`). No `references/` subdirectory. The file MUST be ≤80 lines.

#### Scenario: Skill file location and size
- **WHEN** a guardrail skill is created for domain "core"
- **THEN** it exists at `odoo-v19-core-guard/SKILL.md` and contains ≤80 lines

### Requirement: Skill content — pitfalls only
Each guardrail skill MUST contain ONLY v19-specific pitfalls and breaking changes. It SHALL NOT contain general Odoo tutorials, workflow diagrams, field lists, or extension pattern examples.

#### Scenario: No tutorial content
- **WHEN** a guardrail skill is reviewed
- **THEN** it contains no sections titled "Business Context", "Workflow", "Key Models", "Extension Patterns", or similar instructive content

### Requirement: Skill sections
Each guardrail skill MUST have these sections: "Hard Failures" (install-crashing pitfalls), "Wrong Patterns" (deprecated but installable patterns), and "v19-Specific Syntax" (syntax changes from previous versions).

#### Scenario: Required sections present
- **WHEN** a guardrail skill is created
- **THEN** it contains `## Hard Failures`, `## Wrong Patterns`, and `## v19-Specific Syntax` sections

### Requirement: Pitfall entry format in skill
Each pitfall in the skill MUST use a concise "wrong → right" format showing what NOT to do and what to do instead.

#### Scenario: Pitfall format
- **WHEN** a pitfall is written in the skill
- **THEN** it shows the wrong pattern and the correct v19 alternative in a scannable format (not multi-paragraph explanations)

### Requirement: YAML frontmatter
Each skill MUST have valid YAML frontmatter with `name` and `description` fields. The description MUST include activation keywords (model names, task keywords, module names).

#### Scenario: Frontmatter validation
- **WHEN** a guardrail skill frontmatter is parsed
- **THEN** it has `name: odoo-v19-{domain}-guard` and a `description` field containing relevant Odoo keywords for activation

### Requirement: Three guardrail skills
Phase 2 SHALL produce exactly 3 guardrail skills: `odoo-v19-core-guard`, `odoo-v19-views-guard`, `odoo-v19-sale-guard`.

#### Scenario: All three skills exist
- **WHEN** Phase 2 is complete
- **THEN** `odoo-v19-core-guard/SKILL.md`, `odoo-v19-views-guard/SKILL.md`, and `odoo-v19-sale-guard/SKILL.md` all exist and meet all requirements above
