## ADDED Requirements

### Requirement: Test prompt files
The system SHALL have individual test prompt files stored at `tests/prompts/{domain}/NN-description.md` where domain is one of `core`, `views`, `sale`. Each file MUST contain the prompt text and a verification checklist. There MUST be at least 5 prompts per domain (15+ total).

#### Scenario: Prompt file structure
- **WHEN** a test prompt file is created
- **THEN** it contains a `## Prompt` section with the exact text to send to the model, and a `## Verify` section with a checklist of expected behaviors

#### Scenario: Domain coverage
- **WHEN** all prompt files are counted
- **THEN** there are at least 5 in `tests/prompts/core/`, 5 in `tests/prompts/views/`, and 5 in `tests/prompts/sale/`

### Requirement: Baseline generation
The system SHALL support running each test prompt against a target model (Opus/Sonnet) WITHOUT any skills loaded, generating a complete Odoo module in `addons/`.

#### Scenario: Generate module from prompt
- **WHEN** a test prompt is run against the model without skills
- **THEN** a complete Odoo module is generated in `addons/` with `__manifest__.py`, models, and views as specified by the prompt

### Requirement: Docker install validation
The system SHALL validate each generated module by installing it in the Docker Odoo 19 CE instance using `tests/test_install.sh`.

#### Scenario: Successful install
- **WHEN** a generated module is installed via `docker compose exec odoo-ce odoo -i <module> --stop-after-init`
- **THEN** the output contains "Module <module> loaded" and no ERROR/Traceback lines

#### Scenario: Failed install
- **WHEN** a generated module fails to install
- **THEN** the error type (ParseError, ValueError, ImportError, etc.) and error message are captured for the pitfall catalog

### Requirement: Failure categorization
Each test result MUST be categorized as one of: `HARD_FAIL` (install crashes), `WRONG_PATTERN` (installs but uses incorrect v19 pattern), or `CORRECT` (model gets it right).

#### Scenario: Hard fail categorization
- **WHEN** a module install produces an ERROR or Traceback
- **THEN** it is categorized as `HARD_FAIL`

#### Scenario: Wrong pattern categorization
- **WHEN** a module installs successfully but the code uses deprecated patterns (e.g., `<tree>` instead of `<list>`, domain syntax for `invisible`)
- **THEN** it is categorized as `WRONG_PATTERN`

#### Scenario: Correct categorization
- **WHEN** a module installs successfully and uses correct v19 patterns
- **THEN** it is categorized as `CORRECT` and excluded from the pitfall catalog
