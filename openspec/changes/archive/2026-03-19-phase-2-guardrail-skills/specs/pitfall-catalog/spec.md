## ADDED Requirements

### Requirement: Pitfall catalog file
The system SHALL maintain a pitfall catalog at `documents/pitfall-catalog.md` that is the single source of truth for all discovered v19 breaking changes and wrong patterns.

#### Scenario: Catalog exists and is populated
- **WHEN** failure discovery is complete
- **THEN** `documents/pitfall-catalog.md` contains all HARD_FAIL and WRONG_PATTERN entries organized by domain (core, views, sale)

### Requirement: Pitfall entry format
Each pitfall entry MUST include: a category (`HARD_FAIL` or `WRONG_PATTERN`), what the model generated (wrong), what v19 requires (correct), and which test prompt(s) triggered it.

#### Scenario: Hard fail entry
- **WHEN** a HARD_FAIL pitfall is documented
- **THEN** it includes the error type, the wrong code/pattern, the correct v19 alternative, and the prompt ID that triggered it

#### Scenario: Wrong pattern entry
- **WHEN** a WRONG_PATTERN pitfall is documented
- **THEN** it includes the deprecated pattern used, the correct v19 pattern, and the prompt ID(s) that triggered it

### Requirement: Consistency validation
A pitfall MUST appear in at least 2 out of 3 runs of the same prompt (or across multiple prompts) to be included in the catalog. One-off random failures SHALL NOT be cataloged.

#### Scenario: Consistent failure included
- **WHEN** a failure occurs in 2+ runs of the same prompt
- **THEN** it is added to the catalog

#### Scenario: One-off failure excluded
- **WHEN** a failure occurs in only 1 run and is not reproduced
- **THEN** it is NOT added to the catalog
