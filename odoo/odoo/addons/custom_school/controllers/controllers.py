# -*- coding: utf-8 -*-
# from odoo import http


# class CustomSchool(http.Controller):
#     @http.route('/custom_school/custom_school', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_school/custom_school/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_school.listing', {
#             'root': '/custom_school/custom_school',
#             'objects': http.request.env['custom_school.custom_school'].search([]),
#         })

#     @http.route('/custom_school/custom_school/objects/<model("custom_school.custom_school"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_school.object', {
#             'object': obj
#         })

