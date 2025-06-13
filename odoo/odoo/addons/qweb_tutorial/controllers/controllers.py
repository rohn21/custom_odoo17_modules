# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json


class QwebTutorial(http.Controller):
    @http.route('/qweb-tutorial', auth='public', website=True)
    def index(self, **kw):
        return http.request.render('qweb_tutorial.qweb_html')
        # return "This is the tutorial page using controller"


class TravelData(http.Controller):
    @http.route('/travel-data', auth='public', website=True)
    def travel_booking_info(self, **kwargs):
        retrieve_data = http.request.env['travel.detail'].sudo().search([])
        output = {'data': retrieve_data}
        return http.request.render('qweb_tutorial.booking_details', output)


# test-static-calendar
class TravelCalendarController(http.Controller):

    @http.route('/travel/calendar', auth='public', website=True)
    def show_calendar(self, **kwargs):
        return request.render('qweb_tutorial.custom_calendar_page', {})


# dynamic-events-calendar
class TravelCalendarAPI(http.Controller):

    @http.route('/calendar', auth='public', website=True)
    def travel_events(self, **kwargs):
        # events = request.env['travel.detail'].sudo().search([])
        user_id = request.env.user.partner_id.id
        appointments = request.env['custom.appointment'].sudo().search([('attendee_ids', 'in', [user_id])])
        # return request.redirect('/web#action=qweb_tutorial.action_travel_detail&view_type=calendar')
        return request.render('qweb_tutorial.event_calendar', {
            'events': appointments,
        })
