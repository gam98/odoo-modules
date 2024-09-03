# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class tkn-refund_points(models.Model):
#     _name = 'tkn-refund_points.tkn-refund_points'
#     _description = 'tkn-refund_points.tkn-refund_points'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
