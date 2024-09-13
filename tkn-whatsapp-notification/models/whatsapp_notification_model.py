import logging
import requests
from odoo import models, api

_logger = logging.getLogger(__name__)

class PosOrder(models.Model):
    _inherit = 'pos.order'  
   
    def create_from_ui(self, orders, draft=False):
        # pylint: disable=no-member
        res = super(PosOrder, self).create_from_ui(orders, draft)
        for order in orders:
            existing_order = self.env['pos.order'].search(['|', ('id', '=', order['data'].get('server_id')), ('pos_reference', '=', order['data']['name'])], limit=1)
            if existing_order:
                self.process_order_and_send_messages(existing_order)  
        return res

    @api.model
    def process_order_and_send_messages(self, existing_order):
        order_data = existing_order.read()[0]
        partner_id = order_data['partner_id'][0]
        partner = self.env['res.partner'].search([('id', '=', partner_id)], limit=1)
        if partner:
            messages = self._build_messages(partner, order_data)
            number = self._trim_phone_number(partner.phone)
            for message in messages:
                print(message)
                #self._send_whatsapp(number, message)

    def _trim_phone_number(self, phone):
        if isinstance(phone, str):
            return ''.join(filter(str.isdigit, phone))
        return ''
    
    def _build_messages(self, partner, pos_order):
        """
        Construye el o los mensajes con su contenido para enviar al técnico.
        """
        def _get_redeemed_points(items):
            """
            Calcula los puntos redimidos en la orden.
            """
            reward_product_ids = [item['product_id'][0] for item in items if 'product_id' in item]    

            rewards = self.env['loyalty.reward'].search([('gift_product_id', 'in', reward_product_ids)])

            point_cost_map = {}

            for reward in rewards:
                product_id = reward['gift_product_id'][0]  # Tomar el ID del producto
                point_cost_map[int(product_id)] = reward['point_cost']

            total_points = 0

            for product_id in reward_product_ids:
                if product_id in point_cost_map:
                    total_points += point_cost_map[product_id]
            
            return total_points

        def _format_message(partner_name, order_amount, points_won, total_points, redeemed_points):
            """
            Formatea el mensaje con la información proporcionada.
            """
            greeting = f"¡Hola {partner_name}!👋\n\n"

            if order_amount < 0:
                transaction_message = (
                    f"Haz realizado una devolución de productos en Servicat, por lo que hemos restado {points_won} puntos de tu saldo.\n\n"
                    
                )
            else:
                transaction_type = "redimido" if redeemed_points else "acumulado"
                points = redeemed_points or points_won
                transaction_message = (
                    f"Gracias por tu compra de ${order_amount}. "
                    f"Con esta transacción, has {transaction_type} {points} puntos.\n\n"
                )

            info_message = (
                f"Ahora, tu saldo total de puntos es de {total_points}.\n\n"
                "Recuerda que puedes canjear tus puntos en cualquier momento. "
                "Para más información sobre cómo redimir tus puntos, por favor visita este enlace: https://www.repuestoslineablanca.com\n\n"
                "¡Esperamos verte pronto! Que tengas un gran día."
            )

            return greeting + transaction_message + info_message

        
        line_ids = pos_order['lines']
        lines = self.env['pos.order.line'].browse(line_ids)
        lines_data = lines.read()
        total_redeemed_points = _get_redeemed_points(lines_data)

        loyalty_points_won = pos_order['loyalty_points'] + total_redeemed_points
        total_loyalty_points = partner.loyalty_points

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

        if message_data['order_amount'] < 0:
            refund_message = _format_message(
                message_data['partner_name'],
                message_data['order_amount'],
                message_data['loyalty_points_won'] * -1,
                message_data['total_loyalty_points'],
                None
            )
            return [refund_message]
        if total_redeemed_points >= 1:
            redeemed_points_message = _format_message(
                message_data['partner_name'],
                message_data['order_amount'],
                None,
                message_data['total_loyalty_points'],
                message_data['total_redeemed_points']
            )
            if message_data['loyalty_points_won'] == 0:
                return [redeemed_points_message]
            return [accumulated_points_message, redeemed_points_message]
        return [accumulated_points_message]

    def _send_whatsapp(self, number, message):
        """
        Envia un mensaje predeterminado de whatsapp al numero del cliente vía API de Mercately
        Las variables de entorno son la URL del webhook y el api-key de la cuenta
        """

        mercately_api_url = self.env['ir.config_parameter'].sudo().get_param('MERCATELY_API_URL')
        mercately_api_key = self.env['ir.config_parameter'].sudo().get_param('MERCATELY_API_KEY')
        
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
