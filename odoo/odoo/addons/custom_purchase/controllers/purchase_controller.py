from odoo import http, fields
from odoo.http import request
import json, base64


class CustomPurchaseController(http.Controller):

    @http.route('/api/purchase/orders', type='http', auth='user', methods=['GET'], csrf=False)
    def get_purchase_orders(self, **kwargs):
        orders = request.env['purchase.order'].sudo().search([], limit=20)
        result = [{
            'id': order.id,
            'name': order.name,
            'partner': order.partner_id.name,
            'amount_total': order.amount_total,
            'requester_name': order.requester_name,
            'project_code': order.project_code,
            'delivery_deadline': str(order.delivery_deadline) if order.delivery_deadline else None,
            'is_urgent': order.is_urgent,
            'internal_notes': order.internal_notes
        } for order in orders]
        return request.make_response(json.dumps(result), headers=[('Content-Type', 'application/json')])

    @http.route('/api/purchase/orders', type='http', auth='user', methods=['POST'], csrf=False)
    def create_purchase_order(self, **kwargs):
        # Read JSON data from the request
        data = request.httprequest.get_json()

        # Ensure required fields are present
        if not data.get('partner_id') or not data.get('order_line'):
            return request.make_response(json.dumps({'error': 'Missing required fields'}),
                                         headers=[('Content-Type', 'application/json')], status=400)

        # Create the purchase order
        try:
            order = request.env['purchase.order'].sudo().create({
                'partner_id': data.get('partner_id'),
                'requester_name': data.get('requester_name'),
                'project_code': data.get('project_code'),
                'delivery_deadline': data.get('delivery_deadline'),
                'is_urgent': data.get('is_urgent', False),
                'internal_notes': data.get('internal_notes'),
                'order_line': [(0, 0, {
                    'product_id': line['product_id'],
                    'product_qty': line['product_qty'],
                    'price_unit': line['price_unit'],
                }) for line in data.get('order_line', [])]
            })

            # Return success response with order details
            return request.make_response(
                json.dumps({
                    'id': order.id,
                    'name': order.name,
                    'partner_id': order.partner_id.name,
                    'amount_total': order.amount_total,
                    'delivery_deadline': str(order.delivery_deadline) if order.delivery_deadline else None,
                }),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            # Handle error and return response
            return request.make_response(
                json.dumps({'error': str(e)}),
                headers=[('Content-Type', 'application/json')],
                status=500
            )

    @http.route('/api/purchase/orders/<int:order_id>/send_email', type='http', auth='user', methods=['POST'], csrf=False)
    def send_purchase_order_email(self, order_id):
        order = request.env['purchase.order'].sudo().browse(order_id)
        if not order.exists():
            return json.dumps({'error': 'Purchase Order not found'}), 404

        template = request.env.ref('purchase.email_template_edi_purchase')
        if template:
            template.send_mail(order.id, force_send=True)
            order.write({'state': 'sent'})
            return json.dumps({
                'message': 'Email sent to vendor',
                'new_status': order.state
            })
        return json.dumps({'error': 'Email template not found'}), 500


     # download PO PDF
    # @http.route('/api/purchase/orders/<int:order_id>/report', type='http', auth='user', methods=['GET'], csrf=False)
    # def download_purchase_order_report(self, order_id):
    #     order = request.env['purchase.order'].sudo().browse(order_id)
    #     if not order.exists():
    #         return json.dumps({'error': 'Purchase Order not found'}), 404
    #
    #     pdf = request.env.ref('purchase.action_report_purchase_order')._render_qweb_pdf(order.id)[0]
    #     pdf_base64 = base64.b64encode(pdf)
    #
    #     return request.make_response(pdf, [
    #         ('Content-Type', 'application/pdf'),
    #         ('Content-Disposition', f'attachment; filename="purchase_order_{order.name}.pdf"')
    #     ])

    # confirm-order
    @http.route('/api/purchase/confirm', type='http', auth='user', methods=['POST'], csrf=False)
    def confirm_po(self, **kw):
        # data = json.loads(request.httprequest.data)
        data = request.httprequest.get_json()
        order_id = data.get('order_id')
        po = request.env['purchase.order'].sudo().browse(order_id)

        if not po.exists():
            return request.make_response(json.dumps({"error": "Purchase Order not found."}),
                                         headers=[('Content-Type', 'application/json')])

        po.button_confirm()

        return request.make_response(json.dumps({
            "success": True,
            "message": "Purchase Order confirmed."
        }), headers=[('Content-Type', 'application/json')])

    # validate-order
    @http.route('/api/purchase/validate-order', type='http', auth='user', methods=['POST'], csrf=False)
    def validate_order(self, **kw):
        data = json.loads(request.httprequest.data)
        order_id = data.get('order_id')
        po = request.env['purchase.order'].sudo().browse(order_id)

        if not po.exists():
            return request.make_response(json.dumps({"error": "Purchase Order not found."}),
                                         headers=[('Content-Type', 'application/json')])

        # Confirm the purchase order, it will create related stock moves
        po.button_confirm()

        return request.make_response(json.dumps({
            "success": True,
            "message": "Purchase Order validated and ready for receiving products."
        }), headers=[('Content-Type', 'application/json')])

    # Receive Products - Validate delivery / picking
    @http.route('/api/purchase/receive', type='http', auth='user', methods=['POST'], csrf=False)
    def receive_products(self, **kw):
        data = json.loads(request.httprequest.data)
        order_id = data.get('order_id')
        po = request.env['purchase.order'].sudo().browse(order_id)

        if not po.exists():
            return request.make_response(json.dumps({"error": "Purchase Order not found."}),
                                         headers=[('Content-Type', 'application/json')])

        pickings = po.picking_ids.filtered(lambda p: p.state not in ('done', 'cancel'))

        if not pickings:
            return request.make_response(json.dumps({"error": "No pending pickings for this PO."}),
                                         headers=[('Content-Type', 'application/json')])

        for picking in pickings:
            picking.action_assign()  # Ensure move lines are created

            for move in picking.move_ids_without_package:
                if not move.move_line_ids:
                    move._generate_move_line()
                for move_line in move.move_line_ids:
                    move_line.quantity = move.product_uom_qty
            picking.button_validate()

        return request.make_response(json.dumps({
            "success": True,
            "message": "Products received."
        }), headers=[('Content-Type', 'application/json')])

    @http.route('/api/purchase/create-bill', type='http', auth='user', methods=['POST'], csrf=False)
    def create_vendor_bill(self, **kw):
        data = json.loads(request.httprequest.data)
        order_id = data.get('order_id')
        bill_date = data.get('bill_date', fields.Date.today())  # Use provided date or default to today

        po = request.env['purchase.order'].sudo().browse(order_id)

        if not po.exists():
            return request.make_response(json.dumps({"error": "Purchase Order not found."}),
                                         headers=[('Content-Type', 'application/json')])

        # Confirm PO if not already confirmed
        if po.state != 'purchase':
            po.button_confirm()  # Make sure the PO is confirmed before creating the bill

        # Create bill lines from PO lines
        bill_lines = []
        for line in po.order_line:
            account = line.product_id.product_tmpl_id.get_product_accounts()['expense']
            bill_lines.append((0, 0, {
                'product_id': line.product_id.id,
                'name': line.name,
                'quantity': line.product_qty,
                'price_unit': line.price_unit,
                'tax_ids': [(6, 0, line.taxes_id.ids)],
                'account_id': account.id,
            }))

        # Ensure the purchase journal is selected
        journal = request.env['account.journal'].sudo().search([('type', '=', 'purchase')], limit=1)
        if not journal:
            return request.make_response(json.dumps({"error": "No purchase journal found."}),
                                         headers=[('Content-Type', 'application/json')])

        # Create the bill and link it to the purchase order
        bill = request.env['account.move'].sudo().create({
            'move_type': 'in_invoice',  # Vendor bill type
            'partner_id': po.partner_id.id,  # Vendor partner
            'invoice_origin': po.name,  # Reference to PO
            'purchase_id': po.id,  # Link to purchase order (this is the key part)
            'invoice_line_ids': bill_lines,
            'journal_id': journal.id,
            'date': bill_date,  # Set the invoice date here
        })

        # Log the created bill and verify it's linked correctly
        if bill.purchase_id:
            print(f"Bill {bill.id} is correctly linked to PO: {bill.purchase_id.name}")
        else:
            print(f"Bill {bill.id} is not linked to a PO.")

        # Return success response with bill ID
        return request.make_response(json.dumps({
            "success": True,
            "message": "Vendor bill created.",
            "bill_id": bill.id
        }), headers=[('Content-Type', 'application/json')])

    @http.route('/api/purchase/post-bill', type='http', auth='user', methods=['POST'], csrf=False)
    def post_bill(self, **kw):
        data = json.loads(request.httprequest.data)
        bill_id = data.get('bill_id')
        bill_date = data.get('bill_date')
        bill = request.env['account.move'].sudo().browse(bill_id)

        if not bill.exists() or bill.state != 'draft':
            return request.make_response(json.dumps({"error": "Invalid or non-draft bill."}),
                                         headers=[('Content-Type', 'application/json')])

        # Ensure both date and invoice_date are set
        actual_date = bill_date or fields.Date.today()
        bill.date = actual_date
        bill.invoice_date = actual_date

        try:
            bill.action_post()
        except Exception as e:
            return request.make_response(json.dumps({
                "error": "Failed to post bill",
                "details": str(e)
            }), headers=[('Content-Type', 'application/json')])

        return request.make_response(json.dumps({
            "success": True,
            "message": "Vendor bill posted.",
            "bill_state": bill.state
        }), headers=[('Content-Type', 'application/json')])
