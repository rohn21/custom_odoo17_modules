# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CustomAppointment(models.Model):
    _name = 'custom.appointment'
    _description = 'Custom Appointment'
    _order = 'start_date desc'

    name = fields.Char(string='Event Name', required=True, help="Name of the appointment")
    start_date = fields.Datetime(string='Start Date', required=True, help="Start date and time of the appointment")
    end_date = fields.Datetime(string='End Date', required=True, help="End date and time of the appointment")
    description = fields.Text(string='Description', help="Details about the appointment")
    attendee_ids = fields.Many2many('res.partner', string='Attendees', default=lambda self: [(6, 0, [self.env.user.partner_id.id])])

    @api.model
    def create(self, vals):
        if 'attendee_ids' not in vals or not vals['attendee_ids']:
            vals['attendee_ids'] = [(6, 0, [self.env.user.partner_id.id])]
            print(vals['attendee_ids'])
        return super().create(vals)

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for rec in self:
            if rec.end_date < rec.start_date:
                if rec.end_date <= rec.start_date:
                    raise ValidationError(
                        "End datetime must be after the Start datetime. "
                        "Same-day events are allowed, but time must be later."
                    )
