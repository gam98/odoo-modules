from odoo import models, fields, api
from datetime import datetime, timedelta

class LoyaltyPoints(models.Model):
    _name = 'loyalty.points'
    _description = 'Loyalty Points with Expiration'

    partner_id = fields.Many2one('res.partner', string="Cliente", required=True)
    won_points = fields.Integer(string="Puntos ganados", required=True)
    aux_points = fields.Integer(string="Puntos Auxiliares", required=True, default=0)
    spent_points = fields.Integer(string="Puntos gastados", required=True, default=0)
    accumulation_date = fields.Date(string="Fecha de acumulación", default=fields.Date.today, required=True)
    expiration_date = fields.Date(string="Fecha de expiración", required=True)
    state = fields.Selection([
        ('active', 'Activo'),
        ('expired', 'Expirado'),
    ], string="Estado", default='active')
    order_name = fields.Char(string="Orden", required=True)

    @api.model
    def create(self, vals):
        if 'expiration_date' not in vals:
            EXPIRATION_PERIOD_MONTHS = 6
            vals['expiration_date'] = fields.Date.today() + timedelta(days=30 * EXPIRATION_PERIOD_MONTHS)
        
        record = super(LoyaltyPoints, self).create(vals)

        # Si se especifican puntos gastados en la creación
        if 'spent_points' in vals and vals['spent_points'] > 0:
            print('++++++++++++++++++++++')
            print('Puntos gastados: ', vals['spent_points'])
            print('++++++++++++++++++++++')
            
            # Llamar directamente a _handle_point_redeem_overflow
            record.update_aux_points(vals['spent_points'], record)

        return record
    
    def update_aux_points(self, redeemed_points, record):
        # Buscar otros registros de puntos activos para el mismo cliente
        records_to_adjust = self.search([
            ('partner_id', '=', record.partner_id.id),
            ('id', '!=', record.id),
            ('state', '=', 'active'),
        ], order='id')

        print('records_to_adjust -> ', records_to_adjust.read())

        # Ajustar los puntos auxiliares de los registros
        for adjust_record in records_to_adjust:
            if redeemed_points <= 0:
                break

            # Reducir aux_points del siguiente registro si tiene puntos
            if adjust_record.aux_points > 0:
                if adjust_record.aux_points >= redeemed_points:
                    adjust_record.aux_points -= redeemed_points
                    redeemed_points = 0
                else:
                    redeemed_points -= adjust_record.aux_points
                    adjust_record.aux_points = 0

    @api.model
    def get_points_for_partner(self, partner_id):
        result = self.read_group(
            domain=[('partner_id', '=', partner_id), ('state', '=', 'active')],
            fields=['aux_points:sum'],
            groupby=['partner_id']
        )
        
        if result:
            aux_points = result[0].get('aux_points', 0)
            total_points = aux_points
        else:
            total_points = 0

        return total_points

    @api.model
    def _cron_expire_loyalty_points(self):
        today = fields.Date.today()
        expired_points = self.search([
            ('expiration_date', '<', today),
            ('state', '=', 'active')
        ])
        expired_points.write({'state': 'expired'})

        # Notificar a los clientes sobre la expiración de sus puntos
        for point in expired_points:
            point.partner_id.message_post(
                body=f"Se han expirado {point.aux_points} puntos de lealtad el {today}."
            )


class ResPartner(models.Model):
    _inherit = 'res.partner'

    loyalty_points = fields.Integer(compute='_compute_loyalty_points', store=False)

    def _compute_loyalty_points(self):
      for partner in self:
        loyalty_points_model = self.env['loyalty.points']
        active_points = loyalty_points_model.get_points_for_partner(partner.id)
        partner.loyalty_points = active_points