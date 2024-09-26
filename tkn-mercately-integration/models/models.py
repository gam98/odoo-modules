#-*- coding: utf-8 -*-

from odoo import models, http
import requests

# traer el partner por su id
    # traer el telefono
    # puntos
    # codigos de referido

# tener un solo metodo que haga todo eso secuencialmente y se ejecute cada dia o cada x tiempo
    # que compare los puntos o codigos que han cambiado para no actualizar al pedo
    # que actualice los contactos en mercately en un foreach

class MercatelyIntegration(models.Model):
    _name = 'mercately'

    def get_partner_id_from_mercately_by_phone(self, partner_phone):

        mercately_api_key = http.request.env['ir.config_parameter'].sudo().get_param('MERCATELY_API_KEY')

        url = f"https://app.mercately.com/retailers/api/v1/customers/{partner_phone}"

        headers = {"api-key": mercately_api_key, 'User-Agent': 'My User Agent 1.0',}

        response = requests.get(url, headers=headers)

        data = response.json()
        if data['message'] == 'Customer found successfully':
            return data['customer']['id']
        else:
            return data['message']

    def update_partner_points_and_referred_codes_in_mercately(self, partner_mercately_id, new_total_points, new_referred_codes_list):

        url = f"https://app.mercately.com/retailers/api/v1/customers/{partner_mercately_id}"
        mercately_api_key = http.request.env['ir.config_parameter'].sudo().get_param('MERCATELY_API_KEY')

        payload = {
            "custom_fields": [
                {
                "field_name": "puntos",
                "field_content": new_total_points
                },
                {
                "field_name": "codigos",
                "field_content": new_referred_codes_list
                }
            ]
        }

        headers = {
        "Content-Type": "application/json",
        "api-key": mercately_api_key,
        'User-Agent': 'My User Agent 1.0',
        }

        try:
            response = requests.put(url, json=payload, headers=headers)
            data = response.json()
            print(data)
        except:
            print('REQUEST FAILED')

    def get_partner_data_by_id(self, partner_id):
        partner = self.env['res.partner'].browse(partner_id)
        if partner.exists():
            partner_phone = partner.read()[0]['phone_sanitized']
            partner_loyalty_points = 300 #partner.read()[0]['loyalty_points']
            # aca buscar los cupones de referido activos
            partner_coupons = 'cupon111'
            return {'partner_phone':partner_phone,'partner_loyalty_points': partner_loyalty_points, 'partner_coupons': partner_coupons}
        else:
            return False
    
    def update_mercately_partner_info(self, partner_id):
        partner_data = self.get_partner_data_by_id(partner_id)
        if partner_data:
            mercately_partner_id = self.get_partner_id_from_mercately_by_phone(partner_data['partner_phone'])
            self.update_partner_points_and_referred_codes_in_mercately(mercately_partner_id,partner_data['partner_loyalty_points'],partner_data['partner_coupons'])
        else:
            print('Error al actualizar los datos en mercately del cliente con id: ', partner_id)