import logging
import requests
from odoo import models, api
from dotenv import load_dotenv
import os

load_dotenv()
_logger = logging.getLogger(__name__)

class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def _process_payment_lines(self, pos_order, pos_session, draft, existing_payment):   
        partner = self.env['res.partner'].search([('id', '=', pos_order['partner_id'])], limit=1)
        messages = self._build_messages(partner, pos_order)
        number = self._trim_phone_number(partner.phone)
        for message in messages:
            self._send_whatsapp(number, message)

    def _trim_phone_number(self, phone):
        return ''.join(filter(str.isdigit, phone))
    
    def _build_messages(self, partner, pos_order):
        """
        Construye el o los mensajes con su contenido para enviar al técnico.
        """
        def _get_redeemed_points(items):
            """
            Calcula los puntos redimidos en la orden.
            """
            reward_items = [item for item in items if 'reward_id' in item[2]]
            total_redeemed_points = 0

            for item in reward_items:
                product = self.env['loyalty.reward'].browse(item[2]['reward_id'])
                total_redeemed_points += product.point_cost

            return total_redeemed_points

        def _format_message(partner_name, order_amount, points_won, total_points, redeemed_points):
            """
            Formatea el mensaje con la información proporcionada.
            """
            return (
                f"¡Hola {partner_name}!👋\n\n"
                f"Gracias por tu compra de ${order_amount}. "
                f"Con esta transacción, has {'redimido' if redeemed_points else 'acumulado'} {redeemed_points or points_won} puntos. "
                f"Ahora, tu saldo total de puntos es de {total_points}.\n\n"
                "Recuerda que puedes canjear tus puntos en cualquier momento. "
                "Para más información sobre cómo redimir tus puntos, por favor visita este enlace: https://www.repuestoslineablanca.com\n\n"
                "¡Esperamos verte pronto! Que tengas un gran día."
            )

        items = pos_order['lines']
        total_redeemed_points = _get_redeemed_points(items)
        loyalty_points_won = pos_order['loyalty_points'] + total_redeemed_points
        total_loyalty_points = partner.loyalty_points + pos_order['loyalty_points']

        message_data = {
            "partner_name": partner.name,
            "order_amount": pos_order['amount_total'],
            "loyalty_points_won": int(loyalty_points_won),
            "total_loyalty_points": int(total_loyalty_points),
            "total_redeemed_points": int(total_redeemed_points),
        }

        accumulated_points_message = _format_message(
            message_data['partner_name'],
            message_data['order_amount'],
            message_data['loyalty_points_won'],
            message_data['total_loyalty_points'] + message_data['total_redeemed_points'],
            None
        )

        redeemed_points_message = _format_message(
            message_data['partner_name'],
            message_data['order_amount'],
            None,
            message_data['total_loyalty_points'],
            message_data['total_redeemed_points']
        )

        if total_redeemed_points >= 1:
            return [accumulated_points_message, redeemed_points_message]
        return [accumulated_points_message]

    def _send_whatsapp(self, number, message):
        """
        Envia un mensaje predeterminado de whatsapp al numero del cliente vía API de Mercately
        Las variables de entorno son la URL del webhook y el api-key de la cuenta
        """

        mercately_api_url = os.getenv("MERCATELY_API_URL")
        mercately_api_key = os.getenv("MERCATELY_API_KEY")
        
        payload = {
            "phone_number": number,
            "message": message
        }

        headers = requests.utils.default_headers()

        headers.update(
            {
                "api-key": mercately_api_key,
                'User-Agent': 'My User Agent 1.0',
            }
        )
        try:
            response = requests.post(mercately_api_url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
                _logger.error("Error al llamar al webhook de whatsapp: %s", e)
