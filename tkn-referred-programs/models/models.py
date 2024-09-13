# from odoo import models, api

# class PosOrder(models.Model):
#     _inherit = 'pos.order'

#     def create_from_ui(self, orders, draft=False):
#         # pylint: disable=no-member
#         res = super(PosOrder, self).create_from_ui(orders, draft)
#         for order in orders:
#             existing_order = self.env['pos.order'].search(['|', ('id', '=', order['data'].get('server_id')), ('pos_reference', '=', order['data']['name'])], limit=1)
#             if existing_order:
#                 print('existing_order: ', existing_order)
#         return res
