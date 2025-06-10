# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    x_qlty_alert = fields.Boolean(string='Quality alert', compute="_compute_qty_alert", store=True)
    x_status = fields.Char(string="Status", compute='_compute_status', store=True)

    @api.depends('product_qty')
    def _compute_qty_alert(self):
        for record in self:
            record.x_qlty_alert = record.product_qty < 5

    @api.depends('product_qty', 'qty_producing')
    def _compute_status(self):
        for record in self:
            if record.state == 'done':
                record.x_status = 'Completed'
            elif record.qty_producing > 0:
                record.x_status = 'In progress'
            else:
                record.x_status = 'Planned'


class MrpWorkOrder(models.Model):
    _inherit = 'mrp.workorder'

    x_machine_code = fields.Char(string="Machine Code")
    x_shift = fields.Selection([
        ('morning', 'Morning'),
        ('evening', 'Evening'),
        ('night', 'Night'),
    ], string="Shift")