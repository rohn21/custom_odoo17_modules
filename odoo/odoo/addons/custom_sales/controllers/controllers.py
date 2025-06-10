# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, Response
import json
from datetime import datetime, date
import logging

# Create a logger instance
_logger = logging.getLogger(__name__)


def json_default(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

class SalesOrderAPI(http.Controller):

    def _json_response(self, data, status=200):
        return Response(json.dumps(data, default=json_default), status=status, content_type='application/json')

    # custom JSON-RPC API
    # @http.route('/api/sales-order/<int:order_id>', auth='public', methods=['GET'])
    # def get_sales_order(self, order_id):
    #     order = request.env['sale.order'].sudo().browse(order_id)
    #     return Response(json.dumps(order.read()[0]), content_type='application/json')

    # REST APIs
    # create-sales-order
    @http.route('/api/sales-orders', type='http', auth='user', methods=['POST'], csrf=False)
    def create_sales_order(self, **kwargs):
        data = request.httprequest.get_json()
        # _logger.info(f"Received data: {data}")
        try:
            order = request.env['sale.order'].sudo().create({
                'partner_id': data['partner_id'],
                'user_id': data.get('user_id'),
                'x_project_code': data.get('x_project_code'),
                'x_estimated_shipping': data.get('x_estimated_shipping'),
                'order_line': [
                    (0, 0, {
                        'product_id': line['product_id'],
                        'name': line.get('name', ''),
                        'product_uom_qty': line['quantity'],
                        'price_unit': line['price_unit'],
                        'tax_id': [(6, 0, line.get('tax_ids', []))]
                    }) for line in data['order_lines']
                ]
            })
            response_data = {
                'id': order.id,
                'name': order.name,
                'date_order': order.date_order,
                'amount_total': float(order.amount_total),
                'x_project_code': order.x_project_code,
                'x_estimated_shipping': order.x_estimated_shipping.isoformat() if order.x_estimated_shipping else None,
            }
            return self._json_response(response_data, status=201)

        except Exception as e:
            _logger.exception("Failed to create sales order")
            return self._json_response({'error': str(e)}, 400)

    # list-sale-orders
    @http.route('/api/sales-orders', type='http', auth='user', methods=['GET'], csrf=False)
    def list_orders(self):
        orders = request.env['sale.order'].sudo().search([], limit=10)
        data = orders.read(['id', 'name', 'date_order', 'amount_total'])
        return self._json_response(data)

    # retrieve-sales-order
    @http.route('/api/sales-orders/<int:order_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_order(self, order_id):
        order = request.env['sale.order'].sudo().browse(order_id)
        if not order.exists():
            return self._json_response({'error': 'Not found'}, 404)
        return self._json_response(order.read()[0])

    # update-sales-order
    @http.route('/api/sales-orders/<int:order_id>', type='http', auth='user', methods=['PUT'], csrf=False)
    def update_order(self, order_id):
        data = request.httprequest.get_json()
        order = request.env['sale.order'].sudo().browse(order_id)
        if not order.exists():
            return self._json_response({'error': 'Not found'}, 404)
        try:
            order.write({
                'x_project_code': data.get('x_project_code', order.x_project_code),
                'x_estimated_shipping': data.get('x_estimated_shipping', order.x_estimated_shipping),
            })
            return self._json_response({'message': 'Order updated', 'id': order.id})
        except Exception as e:
            _logger.exception("Failed to update sales order")
            return self._json_response({'error': str(e)}, 400)

    # delete-sales-order
    @http.route('/api/sales-orders/<int:order_id>', type='http', auth='user', methods=['DELETE'], csrf=False)
    def delete_order(self, order_id):
        order = request.env['sale.order'].sudo().browse(order_id)
        if not order.exists():
            return self._json_response({'error': 'Not found'}, 404)
        try:
            order.unlink()
            return self._json_response({'message': f'Order {order_id} deleted'}, 200)
        except Exception as e:
            _logger.exception("Failed to delete sales order")
            return self._json_response({'error': str(e)}, 400)

class SaleOrderController(http.Controller):

    @http.route('/api/send_quotation', type='json', auth='user', methods=['POST'], csrf=False)
    def send_quotation(self, **kwargs):
        order_id = kwargs.get('order_id')
        if not order_id:
            return {'error': 'Missing order_id'}

        order = request.env['sale.order'].browse(order_id)
        if not order.exists():
            return {'error': 'Sale Order not found'}

        # Send quotation email
        template = request.env.ref('sale.email_template_edi_sale')
        if template:
            template.send_mail(order.id, force_send=True)
            return {'success': True, 'message': 'Quotation email sent'}
        else:
            return {'error': 'Email template not found'}

    @http.route('/api/confirm-order', type='json', auth='user', methods=['POST'], csrf=False)
    def confirm_order(self, **kwargs):
        order_id = kwargs.get('order_id')
        if not order_id:
            return {'error': 'Missing order_id'}

        order = request.env['sale.order'].browse(order_id)
        if not order.exists():
            return {'error': 'Sale Order not found'}

        order.action_confirm()
        return {'success': True, 'message': 'Sale Order confirmed'}

    @http.route('/api/validate-delivery', type='json', auth='user', methods=['POST'], csrf=False)
    def validate_delivery(self, order_id=None):
        if not order_id:
            return {'error': 'Missing order_id'}

        order = request.env['sale.order'].sudo().browse(order_id)
        if not order.exists():
            return {'error': 'Sale Order not found'}

        for picking in order.picking_ids:
            if picking.state not in ['assigned', 'confirmed']:
                picking.action_assign()
            for move_line in picking.move_line_ids:
                move_line.quantity_done = move_line.move_id.product_uom_qty
            picking.button_validate()
        return {'success': True, 'message': 'Delivery validated'}

    @http.route('/api/create-invoice', type='json', auth='user', methods=['POST'], csrf=False)
    def create_invoice(self, **kwargs):
        order_id = kwargs.get('order_id')
        if not order_id:
            return {'error': 'Missing order_id'}

        order = request.env['sale.order'].browse(order_id)
        if not order.exists():
            return {'error': 'Sale Order not found'}

        invoice = order._create_invoices()
        invoice.action_post()
        return {'success': True, 'message': 'Invoice created and posted', 'invoice_id': invoice.id}

    @http.route('/api/get-order_id', type='json', auth='user', methods=['POST'], csrf=False)
    def get_order_id(self, **kwargs):
        order_name = kwargs.get('order_name')
        if not order_name:
            return {
                'jsonrpc': '2.0',
                'id': None,
                'error': {
                    'code': -32602,
                    'message': 'Invalid params',
                    'data': 'Missing required parameter: order_name'
                }
            }

        order = request.env['sale.order'].sudo().search([('name', '=', order_name)], limit=1)
        if order:
            return {
                'jsonrpc': '2.0',
                'id': None,
                'result': {
                    'order_id': order.id
                }
            }
        else:
            return {
                'jsonrpc': '2.0',
                'id': None,
                'error': {
                    'code': -32602,
                    'message': 'Invalid params',
                    'data': 'Sale Order not found'
                }
            }