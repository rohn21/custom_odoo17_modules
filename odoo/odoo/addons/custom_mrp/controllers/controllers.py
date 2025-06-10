# -*- coding: utf-8 -*-
# from odoo import http


# class CustomMrp(http.Controller):
#     @http.route('/custom_mrp/custom_mrp', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_mrp/custom_mrp/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_mrp.listing', {
#             'root': '/custom_mrp/custom_mrp',
#             'objects': http.request.env['custom_mrp.custom_mrp'].search([]),
#         })

#     @http.route('/custom_mrp/custom_mrp/objects/<model("custom_mrp.custom_mrp"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_mrp.object', {
#             'object': obj
#         })

