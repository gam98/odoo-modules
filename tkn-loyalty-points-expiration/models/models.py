from odoo import models, fields, api
from datetime import datetime, timedelta

class LoyaltyProgramExpiration(models.Model):
    _name = 'loyalty.program.expiration'
    _description = 'Loyalty Program Expiration'

    program_id = fields.Many2one('loyalty.program', string='Loyalty Program', required=True)
    expiration_period_months = fields.Integer(string='Expiration Period (Months)', required=True)

class LoyaltyProgram(models.Model):
    _inherit = 'loyalty.program'

    points_can_expire = fields.Boolean(string='¿Los puntos pueden expirar?')
    expiration_period_months = fields.Integer(string='Periodo de expiración en meses', default=12)

    def action_set_expiration_period(self):
        self.ensure_one()
        if not self.points_can_expire:
            return
        expiration = self.env['loyalty.program.expiration'].search([('program_id', '=', self.id)], limit=1)
        if not expiration:
            expiration = self.env['loyalty.program.expiration'].create({
                'program_id': self.id,
                'expiration_period_months': self.expiration_period_months,
            })
        return expiration

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
        ('redeemed', 'Canjeado')
    ], string="Estado", default='active')
    redeemed_points = fields.Integer(string="Puntos Canjeados", default=0)

    @api.model
    def check_expired(self):
        today = fields.Date.today()
        expired_points = self.search([('expiration_date', '<', today), ('state', '=', 'active')])
        for point in expired_points:
            point.state = 'expired'

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

    def extend_expiration(self, days):
        self.ensure_one()
        if self.state == 'active':
            new_expiration_date = self.expiration_date + timedelta(days=days)
            self.write({'expiration_date': new_expiration_date})
    
# Definir un método en el modelo res.partner para obtener la sumatoria de puntos activos
class ResPartner(models.Model):
    _inherit = 'res.partner'

  # Sobrescribimos el campo loyalty_points como un campo computado
    loyalty_points = fields.Integer(compute='_compute_loyalty_points', store=False)

    def _compute_loyalty_points(self):
      for partner in self:
        loyalty_points_model = self.env['loyalty.points']
        # Sumamos los puntos activos de cada cliente
        active_points = loyalty_points_model.get_points_for_partner(partner.id)
        partner.loyalty_points = active_points

class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def create_from_ui(self, orders, draft=False):
        # Crear las órdenes primero
        order_ids = super(PosOrder, self).create_from_ui(orders, draft)

        # Iterar sobre las órdenes creadas
        for order in self.sudo().browse([o['id'] for o in order_ids]):
            print('--------------------')
            print('\033[91m********* Order!!: ', order.read())
            print('--------------------')
            if order.loyalty_points != 0 and order.partner_id:
                print('\033[91m********* New Loyalty points: ', order.loyalty_points)
                print('\033[91m********* Current Loyalty points: ', order.partner_id.loyalty_points)

                # Actualizar los puntos de lealtad del cliente
                order.partner_id.loyalty_points += order.loyalty_points

                # Guardar los puntos en tu modelo personalizado 'loyalty.points'
                expiration_period_months = order.session_id.config_id.loyalty_id.expiration_period_months or 12  # Puedes ajustar la lógica según tu programa de lealtad
                expiration_date = fields.Date.today() + timedelta(days=30 * expiration_period_months)

                # Crear registro de puntos de lealtad en tu modelo
                self.env['loyalty.points'].create({
                    'partner_id': order.partner_id.id,
                    'points': order.loyalty_points,
                    'accumulation_date': fields.Date.today(),
                    'expiration_date': expiration_date,
                    'state': 'active',
                })

        return order_ids