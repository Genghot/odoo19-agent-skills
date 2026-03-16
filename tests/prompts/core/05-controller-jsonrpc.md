# Test: Controller and JSON-RPC

## Prompt

```
Create a new Odoo 19 module called "api_endpoint" in addons/.
It should have:
1. A controller class with a JSON-RPC endpoint at /api/equipment/list
   that returns all equipment.item records as a list of dicts
2. A second endpoint at /api/equipment/<int:item_id> that returns
   a single equipment item's data
3. Both endpoints require authentication (type='json', auth='user')

This module depends on "equipment_tracking".
```

## Verify

- [ ] Controller inherits from `http.Controller`
- [ ] Uses `@http.route` decorator with correct parameters
- [ ] JSON endpoints use `type='json'` and `auth='user'`
- [ ] Routes use proper URL patterns
- [ ] Controller file imported in `__init__.py` via `controllers/` package
- [ ] `__manifest__.py` does NOT list controller files in `data`
- [ ] Module installs in Docker without errors
