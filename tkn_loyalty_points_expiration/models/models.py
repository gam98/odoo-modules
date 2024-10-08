from odoo import models, fields, api
from datetime import timedelta

class LoyaltyPoints(models.Model):
    _name = 'loyalty.points'
    _description = 'Loyalty Points with Expiration'

    partner_id = fields.Many2one('res.partner', required=True)
    won_points = fields.Integer(required=True)
    aux_points = fields.Integer(required=True, default=0)
    spent_points = fields.Integer(required=True, default=0)
    accumulation_date = fields.Date(default=fields.Date.today, required=True)
    expiration_date = fields.Date(required=True)
    state = fields.Selection([
        ('active', 'Activo'),
        ('expired', 'Expirado'),
    ], default='active')
    order_name = fields.Char(required=True)

    @api.model
    def create(self, vals):
        expiration_days = self.env['ir.config_parameter'].sudo().get_param('EXPIRATION_PERIOD_DAYS')

        if expiration_days:
            expiration_days = int(expiration_days)
            vals['expiration_date'] = fields.Date.today() + timedelta(days=expiration_days)        
        elif 'expiration_date' not in vals:
            EXPIRATION_PERIOD_DAYS = 180
            vals['expiration_date'] = fields.Date.today() + timedelta(days=EXPIRATION_PERIOD_DAYS)
        
        record = super(LoyaltyPoints, self).create(vals)

        if 'spent_points' in vals and vals['spent_points'] > 0:
            record.update_aux_points(vals['spent_points'], record)

        return record
    
    def update_aux_points(self, redeemed_points, record):
        records_to_adjust = self.search([
            ('partner_id', '=', record.partner_id.id),
            ('id', '!=', record.id),
            ('state', '=', 'active'),
        ], order='id')

        for adjust_record in records_to_adjust:
            if redeemed_points <= 0:
                break

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