from odoo import models, fields, api

class LoyaltyCard(models.Model):
    _name = 'loyalty.card'
    _description = 'Loyalty Card'

    client_id = fields.Many2one('res.partner', string="Cliente")
    value = fields.Float(string="Valor")

    @api.model
    def create(self, vals):
        # Aquí puedes agregar lógica adicional si es necesario
        # Por ejemplo, podrías asegurarte de que el valor no sea negativo
        print('------------------------ vals: ', vals)
        # if vals.get('value', 0) <= 0:
        #     raise ValueError("El valor de la gift card debe ser mayor que 0.")
        
        # Crear el registro de la gift card
        gift_card = super(LoyaltyCard, self).create(vals)

        return gift_card