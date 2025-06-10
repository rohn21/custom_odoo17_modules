# -*- coding: utf-8 -*-
# from odoo import http


# class CustomCron(http.Controller):
#     @http.route('/custom_cron/custom_cron', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_cron/custom_cron/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_cron.listing', {
#             'root': '/custom_cron/custom_cron',
#             'objects': http.request.env['custom_cron.custom_cron'].search([]),
#         })

#     @http.route('/custom_cron/custom_cron/objects/<model("custom_cron.custom_cron"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_cron.object', {
#             'object': obj
#         })

