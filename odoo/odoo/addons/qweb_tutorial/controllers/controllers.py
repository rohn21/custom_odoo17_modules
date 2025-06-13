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

# calendar
class TravelCalendarController(http.Controller):

    @http.route('/travel/calendar', auth='public', website=True)
    def show_calendar(self, **kwargs):
        return request.render('qweb_tutorial.custom_calendar_page', {})


class TravelCalendarAPI(http.Controller):

    @http.route('/travel/events', auth='public' , website=True)
    def travel_events(self, **kwargs):
        events = request.env['travel.detail'].sudo().search([])
        # return request.redirect('/web#action=qweb_tutorial.action_travel_detail&view_type=calendar')
        return request.render('qweb_tutorial.travel_event_calendar', {
            'events': events,
        })