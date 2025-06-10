# inventory_product.py
from odoo import models, fields

# class StockRule(models.Model):
#     _inherit = 'stock.rule'
#
#     x_priority_level = fields.Selection([
#         ('low', 'Low'), ('medium', 'Medium'), ('high', 'High')
#     ], string="Replenishment Priority")

class StockInventoryLine(models.Model):
    _inherit = 'stock.quant'

    x_qc_passed = fields.Boolean(string='QC Passed')