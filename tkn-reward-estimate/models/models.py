from odoo import models, fields, api

class LoyaltyReward(models.Model):
    _inherit = 'loyalty.reward'

    # price = fields.Float(string="Price")
    percentage = fields.Float(string="Percentage")
    add_points_method = fields.Selection([
        ('manual', 'Manualmente'),
        ('automatic', 'Automático'),
    ], string="¿Cómo desea agregar los puntos?", default='manual')
    is_promotional = fields.Boolean(string="¿Es promocional?")

    @api.onchange('add_points_method', 'percentage', 'gift_product_id', 'is_promotional')
    def _onchange_calculate_point_cost(self):
      for reward in self:
          if reward.add_points_method == 'automatic' and reward.gift_product_id and reward.percentage:
              price = reward.gift_product_id.standard_price if reward.is_promotional else reward.gift_product_id.list_price
              reward.point_cost = (price / reward.percentage) * 100
          else:
              reward.point_cost = 0.0 if reward.add_points_method == 'automatic' else reward.point_cost