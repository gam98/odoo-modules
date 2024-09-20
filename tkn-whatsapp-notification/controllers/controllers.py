from odoo import http
import requests

class MercatelyProxyController(http.Controller):
    @http.route('/mercately/send_message', type='json', auth='user')
    def send_message(self, number, message):
        """
        Envia un mensaje predeterminado de whatsapp al numero del cliente vía API de Mercately
        Las variables de entorno son la URL del webhook y el api-key de la cuenta
        """
        mercately_api_url = http.request.env['ir.config_parameter'].sudo().get_param('MERCATELY_API_URL')
        mercately_api_key = http.request.env['ir.config_parameter'].sudo().get_param('MERCATELY_API_KEY')
        
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

        response = requests.post(mercately_api_url, json=payload, headers=headers)
        return response.json()
