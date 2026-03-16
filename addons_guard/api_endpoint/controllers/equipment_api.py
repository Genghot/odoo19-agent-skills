from odoo import http
from odoo.http import request


class EquipmentApiController(http.Controller):

    @http.route('/api/equipment/list', type='json', auth='user', methods=['POST'])
    def equipment_list(self):
        items = request.env['equipment.item'].search([])
        return [
            {
                'id': item.id,
                'name': item.name,
                'serial_number': item.serial_number or '',
                'purchase_date': item.purchase_date.isoformat() if item.purchase_date else False,
                'status': item.status,
                'assigned_to': item.assigned_to.name or False,
            }
            for item in items
        ]

    @http.route('/api/equipment/<int:item_id>', type='json', auth='user', methods=['POST'])
    def equipment_detail(self, item_id):
        item = request.env['equipment.item'].browse(item_id)
        if not item.exists():
            return {'error': 'Equipment item not found'}
        return {
            'id': item.id,
            'name': item.name,
            'serial_number': item.serial_number or '',
            'purchase_date': item.purchase_date.isoformat() if item.purchase_date else False,
            'status': item.status,
            'assigned_to': item.assigned_to.name or False,
            'notes': item.notes or '',
        }
