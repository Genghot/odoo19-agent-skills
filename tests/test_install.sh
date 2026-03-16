#!/bin/bash
# Phase 1 Skills Validation — Install test modules in Docker Odoo CE
# Usage: ./tests/test_install.sh [module_name]
# If no module_name given, tests all modules in addons/

set -euo pipefail

COMPOSE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ADDONS_DIR="$COMPOSE_DIR/addons"
DB_NAME="test_ce"
ODOO_ADDONS_PATH="/mnt/extra-addons/test,/usr/lib/python3/dist-packages/odoo/addons"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

pass=0
fail=0
skip=0

install_module() {
    local module="$1"
    local module_path="$ADDONS_DIR/$module"

    if [ ! -f "$module_path/__manifest__.py" ]; then
        echo -e "${YELLOW}SKIP${NC} $module — no __manifest__.py"
        ((skip++))
        return
    fi

    echo -n "Installing $module... "

    output=$(docker compose -f "$COMPOSE_DIR/docker-compose.yml" exec -T odoo-ce \
        odoo -d "$DB_NAME" \
        --db_host=db --db_user=odoo --db_password=odoo \
        --addons-path="$ODOO_ADDONS_PATH" \
        -i "$module" --stop-after-init 2>&1)

    if echo "$output" | grep -q "Module $module loaded"; then
        echo -e "${GREEN}PASS${NC}"
        ((pass++))
    elif echo "$output" | grep -q "invalid module names.*$module"; then
        echo -e "${RED}FAIL${NC} — module not found in addons path"
        ((fail++))
    elif echo "$output" | grep -qi "error\|traceback\|exception"; then
        echo -e "${RED}FAIL${NC}"
        echo "$output" | grep -i "error\|traceback" | tail -5
        ((fail++))
    else
        echo -e "${YELLOW}WARN${NC} — unclear result, check logs"
        echo "$output" | tail -3
        ((fail++))
    fi
}

# Ensure containers are running
if ! docker compose -f "$COMPOSE_DIR/docker-compose.yml" ps --status running | grep -q odoo-ce; then
    echo "Starting Odoo CE..."
    docker compose -f "$COMPOSE_DIR/docker-compose.yml" up db odoo-ce -d
    echo "Waiting for Odoo to initialize..."
    sleep 15
fi

echo "═══════════════════════════════════════"
echo "  Phase 1 — Module Install Validation"
echo "═══════════════════════════════════════"
echo ""

if [ $# -gt 0 ]; then
    # Test specific module
    install_module "$1"
else
    # Test all modules in addons/
    if [ -z "$(ls -A "$ADDONS_DIR" 2>/dev/null)" ]; then
        echo "No modules found in $ADDONS_DIR"
        exit 1
    fi
    for module_dir in "$ADDONS_DIR"/*/; do
        module=$(basename "$module_dir")
        install_module "$module"
    done
fi

echo ""
echo "═══════════════════════════════════════"
echo -e "  Results: ${GREEN}$pass passed${NC}, ${RED}$fail failed${NC}, ${YELLOW}$skip skipped${NC}"
echo "═══════════════════════════════════════"

exit $fail
