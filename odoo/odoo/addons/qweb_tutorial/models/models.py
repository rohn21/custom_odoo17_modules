# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TravelDetail(models.Model):
    _name = 'travel.detail'
    _description = 'Travel Booking Detail'

    name = fields.Char(string='Event name')
    partner_id = fields.Many2one('res.partner', string='Customer')
    partner_mobile = fields.Char(string='Mobile Number')
    passenger_count = fields.Integer(string='Number of Passengers')
    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string="End Date")
