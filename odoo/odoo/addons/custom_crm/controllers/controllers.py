# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, Response
import json

class CustomCrmController(http.Controller):

    @http.route('/api/crm/custom_leads', auth='user', type='http', methods=['GET'], csrf=False)
    def get_vip_leads(self):
        leads = request.env['crm.lead'].sudo().search([('is_vip_lead', '=', True)])
        data = [{'id': l.id, 'name': l.name} for l in leads]
        return Response(json.dumps(data), content_type='application/json', status=200)