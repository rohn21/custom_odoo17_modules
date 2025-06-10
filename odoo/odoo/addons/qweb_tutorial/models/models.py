# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class qweb_tutorial(models.Model):
#     _name = 'qweb_tutorial.qweb_tutorial'
#     _description = 'qweb_tutorial.qweb_tutorial'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

