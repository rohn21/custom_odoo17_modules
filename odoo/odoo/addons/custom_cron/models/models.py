# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)

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


class SaleOrderCron(models.Model):
    _inherit = 'sale.order'

    @api.model
    def auto_archive_old_sales(self):
        days_threshold = 90
        cutoff_date = fields.Date.to_string(datetime.today() - timedelta(days=days_threshold))

        old_orders = self.search([
            ('state', '=', 'sale'),
            ('date_order', '<=', cutoff_date),
        ])

        if old_orders:
            _logger.info(f"[CRON] Archiving {len(old_orders)} old confirmed sale orders (before {cutoff_date})")
            old_orders.write({'name': lambda self: self.name + ' (Archived)'})
        else:
            _logger.info("[CRON] No old sale orders found to archive.")
