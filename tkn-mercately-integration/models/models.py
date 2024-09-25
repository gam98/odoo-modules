# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class tkn-mercately-integration(models.Model):
#     _name = 'tkn-mercately-integration.tkn-mercately-integration'
#     _description = 'tkn-mercately-integration.tkn-mercately-integration'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
