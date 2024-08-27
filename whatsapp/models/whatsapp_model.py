import logging
import requests
from odoo import models, api

_logger = logging.getLogger(__name__)

class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def _process_payment_lines(self, pos_order, pos_session, draft, existing_payment):        
        partner = self.env['res.partner'].search([('id', '=', pos_order['partner_id'])], limit=1)
        self._send_whatsapp(partner, pos_order)    

    def _send_whatsapp(self, partner, pos_order):
        """
        Envia un mensaje predeterminado de whatsapp al numero del cliente vía API de Mercately
        """
        # TO DO: hacer numero dinámico, tomar api-key y url de .env, refactorizar, agregar timeout en el trysss completar manifest del modulo
        
        url = "https://app.mercately.com/retailers/api/v1/whatsapp/send_message"
        loyalty_points_won = pos_order['loyalty_points']
        total_loyalty_points = partner.loyalty_points + loyalty_points_won

        message_data = {
             "partner_name": partner.name,
             "order_amount": pos_order['amount_total'],
             "loyalty_points_won": int(loyalty_points_won),
             "total_loyalty_points": int(total_loyalty_points),
             "cellphone_number": '5493517738898' 
        }

        message = (
            f"¡Hola {message_data['partner_name']}!👋\n\n"
            f"Gracias por tu compra de ${message_data['order_amount']}. "
            f"Con esta transacción, has acumulado {message_data['loyalty_points_won']} puntos. "
            f"Ahora, tu saldo total de puntos es de {message_data['total_loyalty_points']}.\n\n"
            "Recuerda que puedes canjear tus puntos en cualquier momento. "
            "Para más información sobre cómo redimir tus puntos, por favor visita este enlace: https://www.google.com\n\n"
            "¡Esperamos verte pronto! Que tengas un gran día."
        )

        payload = {
            "phone_number": message_data['cellphone_number'],
            "message": message
        }

        headers = requests.utils.default_headers()

        headers.update(
            {
                "api-key": "1b3a59f063881b48208d4a7bbf37831c",
                'User-Agent': 'My User Agent 1.0',
            }
        )
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
                _logger.error("Error al llamar al webhook de whatsapp: %s", e)
