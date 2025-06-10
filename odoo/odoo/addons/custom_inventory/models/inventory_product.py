# inventory_product.py
from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    x_storage_condition = fields.Selection([
        ('normal', 'Normal'),
        ('cool', 'Cool Storage'),
        ('freeze', 'Freezer'),
    ], string='Storage Condition')
