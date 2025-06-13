# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json


class WebsiteAppointmentController(http.Controller):

    @http.route('/api/appointment/create', type='http', auth='user', methods=['POST'], csrf=False, website=True)
    def create_appointment(self, **kwargs):
        try:
            data = json.loads(request.httprequest.data)
            name = data.get('name')
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            description = data.get('description')
            print(start_date)

            if not name:
                return request.make_response(
                    json.dumps({'success': False, 'error': 'Name is required'}),
                    headers=[('Content-Type', 'application/json')]
                )

            start_date = start_date.replace('T', ' ')
            end_date = end_date.replace('T', ' ')

            appointment = request.env['custom.appointment'].sudo().create({
                'name': name,
                'start_date': start_date,
                'end_date': end_date,
                'description': description,
            })
            print(f"start date", appointment.start_date)
            return request.make_response(
                json.dumps({'success': True, 'id': appointment.id}),
                headers=[('Content-Type', 'application/json')]
            )

        except Exception as e:
            return request.make_response(
                json.dumps({'success': False, 'error': str(e)}),
                headers=[('Content-Type', 'application/json')]
            )
