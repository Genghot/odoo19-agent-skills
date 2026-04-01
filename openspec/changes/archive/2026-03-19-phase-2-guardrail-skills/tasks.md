## 1. Test Prompt Expansion

- [x] 1.1 Create `tests/prompts/core/` directory with 5+ prompt files: module scaffold, model inheritance, security groups + ACL, wizard/transient model, controller + JSON-RPC
- [x] 1.2 Create `tests/prompts/views/` directory with 5+ prompt files: form + list view, kanban view, search view + filters, XPath inheritance, settings/config view
- [x] 1.3 Create `tests/prompts/sale/` directory with 5+ prompt files: extend sale.order, override action_confirm, customize invoice line, pricelist extension, sale report/QWeb

## 2. Baseline Failure Discovery

- [x] 2.1 Run all core prompts against Opus WITHOUT skills, save generated modules in `addons/`
- [x] 2.2 Install all core-generated modules in Docker CE, record pass/fail and error details
- [x] 2.3 Run all views prompts against Opus WITHOUT skills, save generated modules
- [x] 2.4 Install all views-generated modules in Docker CE, record pass/fail and error details
- [x] 2.5 Run all sale prompts against Opus WITHOUT skills, save generated modules
- [x] 2.6 Install all sale-generated modules in Docker CE, record pass/fail and error details
- [x] 2.7 Review installed-but-wrong modules for WRONG_PATTERN issues (deprecated syntax, incorrect v19 patterns)

## 3. Pitfall Catalog

- [x] 3.1 Compile all HARD_FAIL entries from Docker install failures into `documents/pitfall-catalog.md`
- [x] 3.2 Compile all WRONG_PATTERN entries from code review into the catalog
- [x] 3.3 Verify consistency: re-run failing prompts to confirm each pitfall reproduces (2+ out of 3 runs)
- [x] 3.4 Remove one-off failures that don't reproduce consistently

## 4. Write Guardrail Skills

- [x] 4.1 Create `odoo-v19-core-guard/SKILL.md` from catalog core pitfalls (67 lines)
- [x] 4.2 Create `odoo-v19-views-guard/SKILL.md` from catalog views pitfalls (82 lines)
- [x] 4.3 Create `odoo-v19-sale-guard/SKILL.md` from catalog sale pitfalls (76 lines)
- [x] 4.4 Verify each skill has sections: Hard Failures, Wrong Patterns, v19-Specific Syntax
- [x] 4.5 Verify each skill ≤80 lines and contains no tutorial/instructive content

## 5. Guardrail Validation

- [x] 5.1 Re-run ALL prompts WITH guardrail skills loaded, save generated modules
- [x] 5.2 Install all guardrail-generated modules in Docker CE, record pass/fail
- [x] 5.3 Review guardrail-generated code for correct v19 patterns (verification checklists)
- [x] 5.4 Compare: guardrails vs baseline — accuracy (passes), cost ($), output tokens
- [x] 5.5 Write comparison report to `documents/phase2-results.md`
- [x] 5.6 If any guardrail skill hurts accuracy: identify, revise or remove, re-test

## 6. Cleanup

- [x] 6.1 Archive Phase 1 verbose skills (move to `archive/` or add README noting they're superseded)
- [x] 6.2 Update `documents/roadmaps/odoo19-agent-skills.md` with Phase 2 results
- [x] 6.3 Commit and push all Phase 2 artifacts
