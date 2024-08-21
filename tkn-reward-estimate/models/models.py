from odoo import models, fields, api

class LoyaltyReward(models.Model):
    _inherit = 'loyalty.reward'

    # price = fields.Float(string="Price")
    percentage = fields.Float(string="Percentage")
    # points_required = fields.Float(string="Points Required", compute="_compute_points_required")

    @api.onchange('percentage', 'gift_product_id')
    def _onchange_calculate_point_cost(self):
        for reward in self:
            if reward.gift_product_id and reward.percentage:
                # Suponiendo que el costo del producto es el precio de venta
                # print('reward.gift_product_id -> ',reward.gift_product_id.standard_price)
                # print('reward.gift_product_id -> ',reward.gift_product_id.list_price)
                # print('reward.gift_product_id -> ',reward.gift_product_id.categ_id.name)

                if(reward.gift_product_id.categ_id.name == 'Promocionales'):
                  reward.point_cost = (reward.gift_product_id.standard_price / reward.percentage) * 100
                else:
                  reward.point_cost = (reward.gift_product_id.list_price / reward.percentage) * 100
            else:
                reward.point_cost = 0.0

    # @api.depends('price', 'percentage')
    # def _compute_points_required(self):
    #     for reward in self:
    #         if reward.price and reward.percentage:
    #             reward.points_required = reward.price * (reward.percentage / 100)
    #         else:
    #             reward.points_required = 0.0
