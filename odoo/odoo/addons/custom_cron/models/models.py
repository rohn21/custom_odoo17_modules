# -*- coding: utf-8 -*-

from odoo import models, fields, api


class custom_cron(models.Model):
    _name = 'custom.cron.model'
    _description = 'Custom model to test cron job'

    name = fields.Char(string="Name")
    last_run = fields.Datetime(string="Last Run")

    def action_cron_test_method(self):
        self.create({
            'name': 'Cron Executed',
            'last_run': fields.Datetime.now()
        })
