## Context

This is a greenfield project creating Agent Skills for Odoo v19. No skills exist yet. The Odoo 19 Community source is available at `/Users/administrator/Developer/odoo_19/odoo/` with 596 addons, the ORM framework under `odoo/orm/` and `odoo/models/`, and the base module at `odoo/addons/base/`.

Skills follow the open [Agent Skills](https://agentskills.io) standard: a `SKILL.md` with YAML frontmatter (name, description, metadata) and markdown body, plus optional `references/` directory for deep-dive content. Both Claude Code and Google Antigravity discover skills via this format.

Phase 1 builds 3 skills: `odoo-v19-core`, `odoo-v19-views`, `odoo-v19-sale`.

## Goals / Non-Goals

**Goals:**

- Produce 3 working skills that agents can discover and activate
- Each SKILL.md stays under 5K tokens (~400 lines) to respect context budgets
- Each reference file stays under 3K tokens (~250 lines)
- Content is accurate to Odoo 19 Community source code (not documentation or older versions)
- Smart descriptions enable reliable skill activation on relevant prompts
- Establish the content blueprint/template that Phase 2+ skills will follow

**Non-Goals:**

- Enterprise edition content (Phase 4)
- OWL/JavaScript framework skill (Phase 2)
- Automated CI validation of skill content
- Scripts or executable code within skills
- Cross-module integration patterns (Phase 3)

## Decisions

### 1. Content extraction: AI reads source, human reviews

**Decision**: Use Claude to read actual Odoo 19 `.py` and `.xml` source files and extract model definitions, field types, workflow states, view patterns, and method signatures. Human reviews for accuracy and adds tribal knowledge (pitfalls, "don't do this" patterns).

**Alternatives considered**:
- Pure manual writing: Too slow for the breadth needed
- Scraping Odoo docs: Docs lag behind source and lack implementation detail
- Copy-pasting source code: Violates token budget; skills should synthesize, not dump

### 2. Include concise code examples in SKILL.md

**Decision**: Yes — include 2-3 minimal code examples per skill (field declaration, method override, view extension). Keep examples under 10 lines each.

**Rationale**: Code examples dramatically improve agent output quality. The token cost (~200 tokens per example) is worth it. Move longer examples to `references/` if needed.

**Alternatives considered**:
- No examples (pure prose): Agents produce less accurate code without patterns to follow
- Extensive examples: Blows token budget; belongs in references/

### 3. Cross-module references via "See also" links, not inline content

**Decision**: When `odoo-v19-sale` needs to reference accounting concepts (e.g., `_prepare_invoice_line`), include a brief description and a "See also: odoo-v19-account" pointer. Don't duplicate content across skills.

**Rationale**: Keeps each skill self-contained within token budget. Agents can activate additional skills if needed.

### 4. SKILL.md structure follows the blueprint from the roadmap

**Decision**: Every SKILL.md uses this section order:
1. Business Context
2. Workflow (ASCII state diagram)
3. Key Models & Relations (model graph + key fields/methods)
4. Extension Patterns (how to customize)
5. Common Pitfalls
6. Sub-module Map
7. References (links to references/*.md)

**Rationale**: Consistency across skills makes them predictable for both agents and humans maintaining them.

### 5. Reference file granularity: one file per concern, not per model

**Decision**: Reference files are organized by topic (e.g., `field-types.md`, `order-workflow.md`) rather than one file per model. A single reference file may cover multiple related models.

**Rationale**: Topic-based organization matches how agents look up information ("how does invoicing work?" not "tell me about account.move.line"). Reduces file count and keeps each file focused.

### 6. Description keywords include model `_name` values

**Decision**: Every skill description includes the technical `_name` values of key models (e.g., `sale.order`, `sale.order.line`) alongside business terms (quotation, sales order).

**Rationale**: Agents match skills against user prompts. Users may say "sale.order" or "quotation" — descriptions must catch both.

## Risks / Trade-offs

- **Stale content if Odoo 19 source changes** → Pin `odoo-version: "19.0"` in metadata. Re-extract on point releases.
- **SKILL.md exceeds 5K token budget** → Aggressively move detail to references/. Use bullet lists over prose. Measure token count during review.
- **Descriptions too narrow → skills don't activate** → Test activation with 10+ diverse prompts per skill during review. Include synonyms and related terms.
- **Code examples become wrong patterns** → Verify every example compiles against actual Odoo 19 patterns. Keep examples minimal so there's less to go wrong.
- **Sale skill too shallow without account/stock context** → Include brief workflow integration notes ("after confirmation, creates stock.picking if delivery is configured") without duplicating those skills' content.
