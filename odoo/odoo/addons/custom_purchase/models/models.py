from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    requester_name = fields.Char(string="Requested By")
    project_code = fields.Char(string="Project Code")
    delivery_deadline = fields.Date(string="Delivery Deadline")
    is_urgent = fields.Boolean(string="Urgent Request")
    internal_notes = fields.Text(string="Internal Notes")
