from odoo import http
from odoo.http import request, Response
import json

class InventoryAPI(http.Controller):

    @http.route('/api/products', type='http', auth='user', methods=['POST'], csrf=False)
    def create_product(self, **kwargs):
        product = request.env['product.template'].sudo().create({
            'name': kwargs.get('name'),
            'type': kwargs.get('type', 'product'),
            'list_price': kwargs.get('list_price', 0.0),
            'x_storage_condition': kwargs.get('x_storage_condition'),
            'x_expiry_days': kwargs.get('x_expiry_days'),
        })
        return {'id': product.id, 'message': 'Product created successfully'}

class ProductRESTController(http.Controller):

    def _json_response(self, data, status=200):
        return Response(
            json.dumps(data),
            status=status,
            content_type='application/json;charset=utf-8'
        )

    @http.route('/api/rest/products', type='http', auth='user', methods=['GET'], csrf=False)
    def get_products(self, **kwargs):
        products = request.env['product.template'].sudo().search([])
        result = [{
            'id': p.id,
            'name': p.name,
            'default_code': p.default_code,
            'list_price': p.list_price,
            'standard_price': p.standard_price,
            'type': p.type,
            'uom_id': p.uom_id.id,
            'category_id': p.categ_id.id
        } for p in products]
        return self._json_response(result)

    @http.route('/api/rest/products/<int:product_id>', type='http', auth='user', methods=['GET'], csrf=False)
    def get_product(self, product_id, **kwargs):
        product = request.env['product.template'].sudo().browse(product_id)
        if not product.exists():
            return self._json_response({'error': 'Product not found'}, status=404)
        result = {
            'id': product.id,
            'name': product.name,
            'default_code': product.default_code,
            'list_price': product.list_price,
            'standard_price': product.standard_price,
            'type': product.type,
            'uom_id': product.uom_id.id,
            'category_id': product.categ_id.id
        }
        return self._json_response(result)

    @http.route('/api/rest/products', type='http', auth='user', methods=['POST'], csrf=False)
    def create_product(self, **kwargs):
        try:
            data = json.loads(request.httprequest.data)
            product = request.env['product.template'].sudo().create(data)
            return self._json_response({'id': product.id, 'message': 'Product created'}, status=201)
        except Exception as e:
            return self._json_response({'error': str(e)}, status=400)

    @http.route('/api/rest/products/<int:product_id>', type='http', auth='user', methods=['PUT'], csrf=False)
    def update_product(self, product_id, **kwargs):
        try:
            product = request.env['product.template'].sudo().browse(product_id)
            if not product.exists():
                return self._json_response({'error': 'Product not found'}, status=404)
            data = json.loads(request.httprequest.data)
            product.write(data)
            return self._json_response({'id': product.id, 'message': 'Product updated'})
        except Exception as e:
            return self._json_response({'error': str(e)}, status=400)

    @http.route('/api/rest/products/<int:product_id>', type='http', auth='user', methods=['DELETE'], csrf=False)
    def delete_product(self, product_id, **kwargs):
        product = request.env['product.template'].sudo().browse(product_id)
        if not product.exists():
            return self._json_response({'error': 'Product not found'}, status=404)
        product.unlink()
        return self._json_response({'message': f'Product {product_id} deleted'})

class ProductVariantAPI(http.Controller):

    def _json_response(self, data, status=200):
        return Response(
            json.dumps(data),
            status=status,
            content_type='application/json;charset=utf-8'
        )

    # 1. Create attribute and values
    @http.route('/api/rest/attributes', type='http', auth='user', methods=['POST'], csrf=False)
    def create_attribute(self, **kwargs):
        try:
            data = json.loads(request.httprequest.data)
            attr_vals = {
                'name': data['name'],
                'create_variant': 'always',
                'display_type': data.get('display_type', 'select'),  # e.g., select, radio, color
                'value_ids': [(0, 0, {'name': val}) for val in data.get('values', [])]
            }
            attribute = request.env['product.attribute'].sudo().create(attr_vals)
            return self._json_response({'id': attribute.id, 'name': attribute.name})
        except Exception as e:
            return self._json_response({'error': str(e)}, status=400)

    # 2. Add attributes to a product (generate variants)
    @http.route('/api/rest/products/<int:product_id>/attributes', type='http', auth='user', methods=['POST'], csrf=False)
    def assign_attribute_to_product(self, product_id, **kwargs):
        try:
            data = json.loads(request.httprequest.data)
            template = request.env['product.template'].sudo().browse(product_id)
            if not template.exists():
                return self._json_response({'error': 'Product not found'}, status=404)

            # Each item in attributes list: { "attribute_id": 1, "value_ids": [1, 2] }
            for attr in data.get('attributes', []):
                attribute = request.env['product.attribute'].sudo().browse(attr['attribute_id'])
                if not attribute.exists():
                    return self._json_response({'error': f"Attribute ID {attr['attribute_id']} not found"}, status=404)

                # Validate that value_ids belong to this attribute
                invalid_values = request.env['product.attribute.value'].sudo().browse(attr['value_ids']).filtered(
                    lambda v: v.attribute_id.id != attribute.id
                )

                if invalid_values:
                    return self._json_response({
                        'error': f"The following values do not belong to attribute {attribute.name}: " +
                                 ", ".join(invalid_values.mapped("name"))
                    }, status=400)

                # Proceed with linking
                template.write({
                    'attribute_line_ids': [(0, 0, {
                        'attribute_id': attribute.id,
                        'value_ids': [(6, 0, attr['value_ids'])]
                    })]
                })

            return self._json_response({'message': 'Attributes added. Variants will be auto-generated.'})
        except Exception as e:
            return self._json_response({'error': str(e)}, status=400)

    @http.route('/api/rest/products/<int:product_id>/variants', type='http', auth='user', methods=['GET'], csrf=False)
    def list_product_variants(self, product_id):
        template = request.env['product.template'].sudo().browse(product_id)
        if not template.exists():
            return self._json_response({'error': 'Template not found'}, status=404)

        return self._json_response([
            {
                'id': variant.id,
                'name': variant.display_name,
                'default_code': variant.default_code,
                'standard_price': variant.standard_price,
                'list_price': variant.lst_price
            }
            for variant in template.product_variant_ids
        ])

    @http.route('/api/rest/variants/<int:variant_id>', type='http', auth='user', methods=['PUT'], csrf=False)
    def update_variant_settings(self, variant_id, **kwargs):
        variant = request.env['product.product'].sudo().browse(variant_id)
        if not variant.exists():
            return self._json_response({'error': 'Variant not found'}, status=404)

        data = json.loads(request.httprequest.data)
        allowed_fields = ['list_price', 'standard_price', 'default_code', 'description_sale', 'route_ids', 'tracking']
        write_vals = {k: v for k, v in data.items() if k in allowed_fields}
        variant.write(write_vals)
        return self._json_response({'message': 'Variant updated'})

class ProductVendorController(http.Controller):

    def _json_response(self, data, status=200):
        return Response(
            json.dumps(data),
            status=status,
            content_type='application/json;charset=utf-8'
        )

    @http.route('/api/rest/variants/<int:variant_id>/vendor', type='http', auth='user', methods=['POST'], csrf=False)
    def add_vendor_info(self, variant_id, **kwargs):
        product = request.env['product.product'].sudo().browse(variant_id)
        if not product.exists():
            return self._json_response({'error': 'Variant not found'}, status=404)

        data = json.loads(request.httprequest.data)
        vendor = request.env['res.partner'].sudo().browse(data.get('vendor_id'))
        if not vendor.exists():
            return self._json_response({'error': 'Vendor not found'}, status=404)

        request.env['product.supplierinfo'].sudo().create({
            'partner_id': vendor.id,
            'product_id': product.id,
            'min_qty': data.get('min_qty', 1),
            'price': data.get('price', 0),
            'delay': data.get('delay', 1)
        })

        return self._json_response({'message': 'Vendor info added'})

    @http.route('/api/rest/variants/<int:variant_id>/stock', type='http', auth='user', methods=['GET'], csrf=False)
    def get_variant_stock(self, variant_id):
        product = request.env['product.product'].sudo().browse(variant_id)
        if not product.exists():
            return self._json_response({'error': 'Variant not found'}, status=404)

        quants = request.env['stock.quant'].sudo().search([('product_id', '=', variant_id)])
        stock_by_location = [{
            'location': q.location_id.complete_name,
            'quantity': q.quantity,
            'reserved': q.reserved_quantity,
            'available': q.available_quantity
        } for q in quants]

        return self._json_response({'variant_id': variant_id, 'stock': stock_by_location})

    @http.route('/api/rest/locations', type='http', auth='user', methods=['GET'], csrf=False)
    def list_stock_locations(self):
        locations = request.env['stock.location'].sudo().search([('usage', '=', 'internal')])
        return self._json_response([
            {'id': loc.id, 'name': loc.complete_name}
            for loc in locations
        ])

    @http.route('/api/rest/picking-types', type='http', auth='user', methods=['GET'], csrf=False)
    def list_picking_types(self):
        types = request.env['stock.picking.type'].sudo().search([])
        return Response(json.dumps([
            {
                'id': pt.id,
                'name': pt.name,
                'code': pt.code,
                'default_location_src_id': pt.default_location_src_id.id if pt.default_location_src_id else None,
                'default_location_src': pt.default_location_src_id.name if pt.default_location_src_id else None,
                'default_location_dest_id': pt.default_location_dest_id.id if pt.default_location_dest_id else None,
                'default_location_dest': pt.default_location_dest_id.name if pt.default_location_dest_id else None
            }
            for pt in types
        ]), content_type='application/json;charset=utf-8')

    @http.route('/api/rest/variants/<int:variant_id>/stock', type='http', auth='user', methods=['POST'], csrf=False)
    def create_stock_adjustment(self, variant_id, **kwargs):
        data = json.loads(request.httprequest.data)
        quantity = data.get('quantity')
        location_dest_id = data.get('location_dest_id')
        picking_type_id = data.get('picking_type_id')
        partner_id = data.get('vendor_id')

        if not all([quantity, location_dest_id, picking_type_id]):
            return self._json_response({'error': 'quantity, location_dest_id, and picking_type_id are required'},
                                       status=400)

        product = request.env['product.product'].sudo().browse(variant_id)
        if not product.exists():
            return self._json_response({'error': 'Product not found'}, status=404)

        picking_type = request.env['stock.picking.type'].sudo().browse(picking_type_id)
        if not picking_type.exists():
            return self._json_response({'error': 'Picking type not found'}, status=404)

        src_location_id = picking_type.default_location_src_id.id if picking_type.default_location_src_id else data.get('location_id')
        if not src_location_id:
            return self._json_response({'error': 'Source location not defined in picking type or payload'}, status=400)

        picking = request.env['stock.picking'].sudo().create({
            'picking_type_id': picking_type_id,
            'location_id': src_location_id,
            'location_dest_id': location_dest_id,
            'partner_id': partner_id,
                'move_ids_without_package': [(0, 0, {
                    'name': product.name,
                'product_id': variant_id,
                'product_uom': product.uom_id.id,
                'product_uom_qty': quantity,
                'location_id': src_location_id,
                'location_dest_id': location_dest_id,
            })]
        })

        picking.action_confirm()
        picking.action_assign()

        for move in picking.move_ids:
            move.quantity = move.product_uom_qty

        picking.button_validate()

        return self._json_response({'message': f'Stock for {product.display_name} updated by {quantity} units'})