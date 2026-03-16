# Test: Search View with Filters

## Prompt

```
Create a new Odoo 19 module called "ticket_search" in addons/.
Add a search view for "helpdesk.ticket" (from helpdesk_lite module) with:
1. Search fields for name and assigned_to
2. Filter "My Tickets" showing tickets assigned to current user
3. Filter "High Priority" showing priority in (high, urgent)
4. Filter "Open" showing state not in (resolved, closed)
5. Date filter on create_date
6. Group by: state, priority, assigned_to
Set "My Tickets" and "Open" as default active filters on the action.
This module depends on "helpdesk_lite".
```

## Verify

- [ ] Search view uses `<search>` element
- [ ] `<filter>` elements have `name` and `domain` attributes
- [ ] Date filter uses `date="create_date"` attribute
- [ ] Group-by filters use `context="{'group_by': 'field'}"` syntax
- [ ] Action context has `search_default_my_tickets` and `search_default_open` keys
- [ ] Module installs in Docker without errors
