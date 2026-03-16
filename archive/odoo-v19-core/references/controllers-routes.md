# Odoo 19 Controllers & Routes Reference

## Controller Basics

Controllers handle HTTP requests. They live in `controllers/` directory.

```python
# controllers/__init__.py
from . import main

# controllers/main.py
from odoo import http
from odoo.http import request


class MyController(http.Controller):

    @http.route('/my/endpoint', type='http', auth='user', website=True)
    def my_page(self, **kwargs):
        orders = request.env['sale.order'].search([])
        return request.render('my_module.my_template', {'orders': orders})
```

## @http.route() Parameters

| Parameter | Values | Description |
|-----------|--------|-------------|
| `route` | str or list[str] | URL path(s). Supports werkzeug converters: `<int:id>`, `<string:name>`, `<model("res.partner"):partner>` |
| `type` | `'http'` \| `'jsonrpc'` | Request type. `'json'` is deprecated alias for `'jsonrpc'` |
| `auth` | `'user'` \| `'public'` \| `'bearer'` \| `'none'` | Authentication mode |
| `methods` | list[str] | Allowed HTTP methods: `['GET']`, `['POST']`, `['GET', 'POST']` |
| `cors` | str | CORS origin header value |
| `csrf` | bool | CSRF protection (default True for http, False for jsonrpc) |
| `readonly` | bool | Use read-only DB cursor (for reporting) |
| `website` | bool | Enable website features (template rendering, SEO) |

### Auth modes

- **`'user'`**: Requires authenticated internal user. Most backend endpoints.
- **`'public'`**: Optional auth. Uses public user if not logged in. For website pages.
- **`'bearer'`**: API token via `Authorization: Bearer <token>` header.
- **`'none'`**: No database, no auth. For health checks, static content.

## Common Patterns

### HTTP endpoint (returns rendered page)

```python
@http.route('/my/orders', type='http', auth='user', website=True)
def portal_orders(self, page=1, **kwargs):
    orders = request.env['sale.order'].search(
        [('partner_id', '=', request.env.user.partner_id.id)],
        limit=10, offset=(page - 1) * 10,
    )
    return request.render('my_module.portal_orders', {
        'orders': orders,
        'page': page,
    })
```

### JSON-RPC endpoint (returns JSON)

```python
@http.route('/api/orders', type='jsonrpc', auth='bearer', methods=['POST'])
def api_get_orders(self, domain=None, limit=10):
    # Parameters come from JSON-RPC request body
    orders = request.env['sale.order'].search(domain or [], limit=limit)
    return [{
        'id': o.id,
        'name': o.name,
        'amount': o.amount_total,
    } for o in orders]
```

### File download

```python
@http.route('/my/order/<int:order_id>/pdf', type='http', auth='user')
def download_order_pdf(self, order_id, **kwargs):
    order = request.env['sale.order'].browse(order_id)
    pdf_content, _ = request.env['ir.actions.report']._render_qweb_pdf(
        'sale.action_report_saleorder', [order.id])
    return request.make_response(pdf_content, headers=[
        ('Content-Type', 'application/pdf'),
        ('Content-Disposition', f'attachment; filename=order_{order.name}.pdf'),
    ])
```

### File upload

```python
@http.route('/my/upload', type='http', auth='user', methods=['POST'], csrf=True)
def upload_file(self, file, **kwargs):
    attachment = request.env['ir.attachment'].create({
        'name': file.filename,
        'datas': base64.b64encode(file.read()),
        'res_model': 'sale.order',
        'res_id': int(kwargs.get('order_id', 0)),
    })
    return request.redirect('/my/orders')
```

## Route Converters

```python
# Integer parameter
@http.route('/order/<int:order_id>', ...)
def get_order(self, order_id):  # order_id is int

# String parameter
@http.route('/page/<string:slug>', ...)
def get_page(self, slug):  # slug is str

# Model converter (auto-browse)
@http.route('/order/<model("sale.order"):order>', ...)
def get_order(self, order):  # order is a recordset
```

## Controller Inheritance

Controllers can be extended in other modules:

```python
from odoo.addons.sale.controllers.portal import SalePortal

class CustomSalePortal(SalePortal):

    @http.route()  # inherits route from parent
    def portal_order_page(self, order_id, **kwargs):
        response = super().portal_order_page(order_id, **kwargs)
        # Modify response or add extra context
        return response
```

New `@http.route()` on the override (with no args) inherits the parent's route configuration. You can pass new args to override specific parameters (e.g., `@http.route(auth='public')`).

## The `request` Object

```python
from odoo.http import request

request.env              # Environment (with current user, company, lang)
request.env.user         # Current user (res.users record)
request.env.company      # Current company (res.company record)
request.env.cr           # Database cursor
request.env.context      # Context dict
request.params           # Request parameters (GET/POST merged)
request.httprequest      # Werkzeug request object
request.session          # Session data
request.render(template, values)  # Render QWeb template
request.redirect(url)    # HTTP redirect
request.make_response(data, headers)  # Custom HTTP response
request.not_found()      # 404 response
```
