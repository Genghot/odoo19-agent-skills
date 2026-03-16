# Test: Kanban View

## Prompt

```
Create a new Odoo 19 module called "task_kanban" in addons/.
Add a kanban view for the model "project.milestone" (from project_task_ext module)
grouped by state. Show the name, deadline, responsible_id as an avatar,
and progress bar. Use color coding based on state.
This module depends on "project_task_ext".
```

## Verify

- [ ] Uses `<kanban default_group_by="state">`
- [ ] Template uses `<t t-name="card">` (NOT `t-name="kanban-box"`)
- [ ] `many2one_avatar_user` widget for responsible_id
- [ ] `<footer>` element used correctly
- [ ] No `<div class="oe_kanban_card">` wrapper (old v16 pattern)
- [ ] Module installs in Docker without errors
