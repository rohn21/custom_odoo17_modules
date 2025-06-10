# inventory_product.py
from odoo import models, fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    x_delivery_type = fields.Selection([
        ('standard', 'Standard'),
        ('express', 'Express'),
        ('overnight', 'Overnight')
    ], string="Delivery Type")

    x_special_note = fields.Text(string="Special Note")
    x_transport_reference = fields.Char(string='Transport Reference')
