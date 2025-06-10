# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Example custom fields
    x_barcode = fields.Char(string="Barcode", compute="_compute_barcode", store=True)
    x_project_code = fields.Char(string="Project Code") # x_ - to define custom fields
    x_estimated_shipping = fields.Date(string="Estimated Shipping Date")

    # generates barcode number based on date and sale_order's number
    @api.depends('date_order', 'name')
    def _compute_barcode(self):
        for order in self:
            if order.date_order and order.name:
                order.x_barcode = order.date_order.date().strftime("%Y%m%d") + order.name

    # method not working
    # @api.model
    # def create(self, vals):
    #     res = super(SaleOrder, self).create(vals)
    #     if res.date_order and res.name:
    #         barcode = res.date_order.date().strftime("%Y%m%d") + res.name
    #         res.write({'x_barcode': barcode})
    #     return res