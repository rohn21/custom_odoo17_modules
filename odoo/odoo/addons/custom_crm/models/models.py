from odoo import models, fields, api

import logging

_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    custom_score = fields.Integer(string="Custom Score", compute="_compute_custom_score", store=True)
    is_vip_lead = fields.Boolean(string="VIP Lead", default=False)

    @api.depends('priority')
    def _compute_custom_score(self):
        for record in self:
            # _logger.info(f"Computing score for Lead ID {record.id}, Priority: {record.priority}")
            record.custom_score = 100 if record.priority == '2' else 50
