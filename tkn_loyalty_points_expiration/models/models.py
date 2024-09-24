from odoo import models, fields, api
from datetime import datetime, timedelta

class LoyaltyPoints(models.Model):
    _name = 'loyalty.points'
    _description = 'Loyalty Points with Expiration'

    partner_id = fields.Many2one('res.partner', string="Cliente", required=True)
    points = fields.Integer(string="Puntos totales", required=True)
    won_points = fields.Integer(string="Puntos ganados", required=True)
    spent_points = fields.Integer(string="Puntos gastados", required=True)
    accumulation_date = fields.Date(string="Fecha de acumulación", default=fields.Date.today, required=True)
    expiration_date = fields.Date(string="Fecha de expiración", required=True)
    state = fields.Selection([
        ('active', 'Activo'),
        ('expired', 'Expirado'),
    ], string="Estado", default='active')
    order_id = fields.Many2one('pos.order', string="Orden POS relacionada")

    @api.model
    def create(self, vals):
        if 'expiration_date' not in vals:
            EXPIRATION_PERIOD_MONTHS = 6
            vals['expiration_date'] = fields.Date.today() + timedelta(days=30 * EXPIRATION_PERIOD_MONTHS)
        return super(LoyaltyPoints, self).create(vals)

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
        expired_points.write({'state': 'expired'})

        # Notificar a los clientes sobre la expiración de sus puntos
        for point in expired_points:
            point.partner_id.message_post(
                body=f"Se han expirado {point.points} puntos de lealtad el {today}."
            )

    def name_get(self):
        return [(record.id, f"{record.partner_id.name} - {record.points} puntos") for record in self]

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

    loyalty_points_won = fields.Float(string="Puntos ganados")
    loyalty_points_spent = fields.Float(string="Puntos gastados")

    @api.model
    def _order_fields(self, ui_order):
        fields = super(PosOrder, self)._order_fields(ui_order)

        # Asigna los valores desde ui_order
        fields['loyalty_points_won'] = ui_order.get('loyalty_points_won', 0)
        fields['loyalty_points_spent'] = ui_order.get('loyalty_points_spent', 0)

        print('------------------')
        print('Loyalty Points Won:', fields['loyalty_points_won'])
        print('Loyalty Points Spent:', fields['loyalty_points_spent'])
        print('------------------')

        return fields

    @api.model
    def create_from_ui(self, orders, draft=False):
        order_ids = super(PosOrder, self).create_from_ui(orders, draft)

        for order in self.sudo().browse([o['id'] for o in order_ids]):
            print('------------------')
            print(order.read())
            print('------------------')
            # if order.loyalty_points and order.partner_id:
            #     self.env['loyalty.points'].create({
            #         'partner_id': order.partner_id.id,
            #         'points': order.loyalty_points,
            #         'won_points': order.loyalty_points_won,
            #         'spent_points': order.loyalty_points_spent,
            #         'accumulation_date': fields.Date.today(),
            #         'order_id': order.id,
            #     })

        return order_ids