#!/bin/bash
# Phase 2 Guardrail Skills Validation — Install test modules in Docker Odoo CE
# Tests addons_guard/ modules (generated WITH guardrail skills)

set -uo pipefail

COMPOSE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ADDONS_DIR="$COMPOSE_DIR/addons_guard"
DB_NAME="test_guard"
SERVICE="odoo-guard"
ODOO_ADDONS_PATH="/mnt/extra-addons/test,/usr/lib/python3/dist-packages/odoo/addons"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

pass=0
fail=0
results=()

install_module() {
    local module="$1"
    local module_path="$ADDONS_DIR/$module"

    if [ ! -f "$module_path/__manifest__.py" ]; then
        echo -e "${YELLOW}SKIP${NC} $module — no __manifest__.py"
        return
    fi

    echo -n "Installing $module... "

    output=$(docker compose -f "$COMPOSE_DIR/docker-compose.yml" exec -T "$SERVICE" \
        odoo -d "$DB_NAME" \
        --db_host=db --db_user=odoo --db_password=odoo \
        --addons-path="$ODOO_ADDONS_PATH" \
        -i "$module" --stop-after-init 2>&1)

    if echo "$output" | grep -q "Module $module loaded"; then
        echo -e "${GREEN}PASS${NC}"
        results+=("PASS|$module")
        ((pass++))
    elif echo "$output" | grep -q "Modules loaded"; then
        echo -e "${GREEN}PASS${NC} (loaded)"
        results+=("PASS|$module")
        ((pass++))
    elif echo "$output" | grep -qi "error\|traceback\|exception"; then
        echo -e "${RED}FAIL${NC}"
        error_msg=$(echo "$output" | grep -i "error\|traceback" | tail -3)
        echo "  $error_msg"
        results+=("FAIL|$module|$error_msg")
        ((fail++))
    else
        echo -e "${YELLOW}WARN${NC} — unclear result"
        results+=("FAIL|$module|unclear")
        ((fail++))
    fi
}

# Install in dependency order
MODULES_ORDERED=(
    # Tier 1: no custom deps
    "equipment_tracking"
    "partner_extended"
    "helpdesk_lite"
    # Tier 2: depends on tier 1
    "mass_assign_wizard"
    "api_endpoint"
    "partner_view_ext"
    "ticket_search"
    "equipment_settings"
    # Tier 3: depends on sale (built-in)
    "sale_priority"
    "sale_confirm_check"
    "sale_line_ref"
    "sale_pricelist_note"
    "sale_custom_report"
    # Tier 4: depends on tier 1 + project
    "project_task_ext"
    "task_kanban"
)

echo "═══════════════════════════════════════════════"
echo "  Phase 2 — Guardrail Module Install Validation"
echo "═══════════════════════════════════════════════"
echo ""

for module in "${MODULES_ORDERED[@]}"; do
    install_module "$module"
done

echo ""
echo "═══════════════════════════════════════════════"
echo -e "  Results: ${GREEN}$pass passed${NC}, ${RED}$fail failed${NC} / ${#MODULES_ORDERED[@]} total"
echo "═══════════════════════════════════════════════"
echo ""

# Write results to file
RESULTS_FILE="$COMPOSE_DIR/tests/guard_install_results.txt"
echo "# Guard Install Results — $(date '+%Y-%m-%d %H:%M')" > "$RESULTS_FILE"
for r in "${results[@]}"; do
    echo "$r" >> "$RESULTS_FILE"
done
echo "" >> "$RESULTS_FILE"
echo "Pass: $pass / ${#MODULES_ORDERED[@]}" >> "$RESULTS_FILE"

exit $fail
