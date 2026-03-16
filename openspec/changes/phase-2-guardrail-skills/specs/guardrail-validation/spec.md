## ADDED Requirements

### Requirement: A/B comparison run
The system SHALL support running the full test prompt suite both WITHOUT skills (baseline) and WITH guardrail skills, capturing accuracy, cost, and token counts for each.

#### Scenario: Baseline run
- **WHEN** all prompts are run without skills
- **THEN** each result is recorded with: module name, install status (pass/fail), verification checklist results, cost, output tokens

#### Scenario: Guardrail run
- **WHEN** all prompts are run with guardrail skills loaded
- **THEN** each result is recorded with the same metrics as baseline

### Requirement: Accuracy comparison
The guardrail run MUST achieve accuracy (verification checklist passes) greater than or equal to the baseline run.

#### Scenario: Guardrails match or beat baseline
- **WHEN** baseline scores N passes and guardrail scores M passes
- **THEN** M ≥ N

#### Scenario: Guardrails underperform
- **WHEN** guardrail accuracy is lower than baseline
- **THEN** the failing skill(s) are identified and either revised or removed

### Requirement: Cost comparison
The guardrail run MUST achieve cost savings of at least 15% compared to baseline.

#### Scenario: Cost savings met
- **WHEN** baseline costs $X and guardrail costs $Y
- **THEN** Y ≤ X × 0.85

### Requirement: Docker install success
Every module generated in the guardrail run MUST install successfully in Docker Odoo 19 CE.

#### Scenario: All modules install
- **WHEN** all guardrail-generated modules are installed in Docker
- **THEN** 100% install without ERROR or Traceback

### Requirement: Comparison report
A comparison report MUST be produced summarizing baseline vs guardrail results in a table format.

#### Scenario: Report generated
- **WHEN** both runs are complete
- **THEN** a comparison report exists at `documents/phase2-results.md` with per-test and aggregate metrics
