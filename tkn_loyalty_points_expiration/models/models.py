from odoo import models, fields, api
from datetime import datetime, timedelta

class LoyaltyPoints(models.Model):
    _name = 'loyalty.points'
    _description = 'Loyalty Points with Expiration'

    partner_id = fields.Many2one('res.partner', string="Cliente", required=True)
    points = fields.Integer(string="Puntos", required=True, default=0)
    accumulation_date = fields.Date(string="Fecha de acumulación", default=fields.Date.today, required=True)
    expiration_date = fields.Date(string="Fecha de expiración", required=True)
    state = fields.Selection([
        ('active', 'Activo'),
        ('expired', 'Expirado'),
    ], string="Estado", default='active')

    @api.model
    def get_points_for_partner(self, partner_id):
        result = self.read_group(
            domain=[('partner_id', '=', partner_id), ('state', '=', 'active')],
            fields=['points:sum'], 
            groupby=['partner_id']
        )
        total_points = result[0]['points'] if result else 0
        return total_points
    
    @api.model
    def _cron_expire_loyalty_points(self):
        today = fields.Date.today()
        expired_points = self.search([
            ('expiration_date', '<', today),
            ('state', '=', 'active')
        ])
        print('------------------')
        print('works!!!!')
        print('------------------')
        expired_points.write({'state': 'expired'})
        
        # Opcional: Notificar a los clientes sobre la expiración de sus puntos
        for point in expired_points:
            point.partner_id.message_post(
                body=f"Se han expirado {point.points} puntos de lealtad el {today}."
            )

class ResPartner(models.Model):
    _inherit = 'res.partner'

    loyalty_points = fields.Integer(compute='_compute_loyalty_points', store=False)

    def _compute_loyalty_points(self):
      for partner in self:
        loyalty_points_model = self.env['loyalty.points']
        active_points = loyalty_points_model.get_points_for_partner(partner.id)
        partner.loyalty_points = active_points

class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def create_from_ui(self, orders, draft=False):
        order_ids = super(PosOrder, self).create_from_ui(orders, draft)

        for order in self.sudo().browse([o['id'] for o in order_ids]):
            print('--------------------')
            print('\033[91m********* Order!!: ', order.read())
            print('--------------------')
             # Iterar sobre las líneas de la orden
            for line in order.lines:
                print('\033[92m********* Line: ', line.read())
                
            if order.loyalty_points != 0 and order.partner_id:
                print('\033[91m********* New Loyalty points: ', order.loyalty_points)
                print('\033[91m********* Current Loyalty points: ', order.partner_id.loyalty_points)

                order.partner_id.loyalty_points += order.loyalty_points
                EXPIRATION_PERIOD_MONTHS = 6 
                expiration_date = fields.Date.today() + timedelta(days=30 * EXPIRATION_PERIOD_MONTHS)

                self.env['loyalty.points'].create({
                    'partner_id': order.partner_id.id,
                    'points': order.loyalty_points,
                    'accumulation_date': fields.Date.today(),
                    'expiration_date': expiration_date,
                    'state': 'active',
                })

        return order_ids