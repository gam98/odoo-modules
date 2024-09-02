from odoo import models, fields, api

class LoyaltyReward(models.Model):
    _inherit = 'loyalty.reward'

    percentage = fields.Float(string="Porcentaje", help="Porcentaje para calcular los puntos")
    add_points_method = fields.Selection([
        ('manual', 'Manualmente'),
        ('automatic', 'Automático'),
    ], string="¿Cómo desea agregar los puntos?", default='manual')
    is_promotional = fields.Boolean(string="¿Es promocional?", default=False, help="Si no es promocional, toma el precio de venta al público.")
    cost_price = fields.Float(string="Precio de Costo")
    show_cost_price = fields.Boolean(compute='_compute_show_cost_price')

    @api.depends('is_promotional')
    def _compute_show_cost_price(self):
        for reward in self:
            reward.show_cost_price = reward.is_promotional

    @api.onchange('add_points_method', 'percentage', 'gift_product_id', 'is_promotional', 'cost_price')
    def _onchange_calculate_point_cost(self):
        for reward in self:
            if reward.add_points_method == 'automatic' and reward.gift_product_id and reward.percentage:                
                if reward.is_promotional and reward.cost_price:
                    price = reward.cost_price
                    reward.point_cost = (price / reward.percentage) * 100
                else:
                    price = reward.gift_product_id.list_price
                    reward.point_cost = (price / reward.percentage) * 100
            else:
                reward.point_cost = 0.0 if reward.add_points_method == 'automatic' else reward.point_cost