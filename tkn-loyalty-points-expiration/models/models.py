from odoo import models, fields

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
        """ This method could be triggered by a button or some other event to set the expiration period for a program """
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
