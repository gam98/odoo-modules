#-*- coding: utf-8 -*-

from odoo import models, http
import requests

class MercatelyIntegration(models.Model):
    _name = 'mercately'

    def get_partner_data_from_mercately_by_phone(self, partner_phone):

        mercately_api_key = http.request.env['ir.config_parameter'].sudo().get_param('MERCATELY_API_KEY')
        mercately_url = http.request.env['ir.config_parameter'].sudo().get_param('MERCATELY_CUSTOMERS_CRUD_URL')

        url = f"{mercately_url}{partner_phone}"

        headers = {"api-key": mercately_api_key, 'User-Agent': 'My User Agent 1.0',}

        response = requests.get(url, headers=headers)

        data = response.json()
        if data['message'] == 'Customer found successfully':
            result = {
                'id': data['customer']['id'],
                'points_and_codes': data['customer']['custom_fields']
            }
            return result
        else:
            return data['message']

    def update_partner_points_and_referred_codes_in_mercately(self, partner_mercately_id, payload):

        mercately_url = http.request.env['ir.config_parameter'].sudo().get_param('MERCATELY_CUSTOMERS_CRUD_URL')

        url = f"{mercately_url}{partner_mercately_id}"
        mercately_api_key = http.request.env['ir.config_parameter'].sudo().get_param('MERCATELY_API_KEY')

        headers = {
        "Content-Type": "application/json",
        "api-key": mercately_api_key,
        'User-Agent': 'My User Agent 1.0',
        }

        try:
            response = requests.put(url, json=payload, headers=headers)
            data = response.json()
        except:
            print('REQUEST FAILED')

    def get_partner_data_by_id(self, partner_id):
        partner = self.env['res.partner'].browse(partner_id)
        if partner.exists():
            partner_phone = partner.read()[0]['phone_sanitized']
            partner_loyalty_points = partner.read()[0]['loyalty_points']
            partner_coupons = self._get_coupon_programs_from_partner_id(partner_id)
    
            return {'partner_phone':partner_phone,'partner_loyalty_points': partner_loyalty_points, 'partner_coupons': partner_coupons}
        else:
            return False
    
    def update_mercately_partner_info(self, partner_id):

        partner_data = self.get_partner_data_by_id(partner_id)
        if partner_data:
            mercately_partner_data = self.get_partner_data_from_mercately_by_phone(partner_data['partner_phone'])
            
            mercately_partner_id = mercately_partner_data['id']

            mercately_codes = next((item['field_content:'] for item in mercately_partner_data['points_and_codes'] if item['field_name'] == 'codigos'), None)
            mercately_points = next((item['field_content:'] for item in mercately_partner_data['points_and_codes'] if item['field_name'] == 'puntos'), None)
            
            odoo_codes = partner_data['partner_coupons']
            odoo_points = partner_data['partner_loyalty_points']
            
            payload = { "custom_fields": []}
            should_update_customer = False

            if mercately_codes != odoo_codes:
                payload["custom_fields"].append({
                "field_name": "codigos",
                "field_content": odoo_codes
                })
                should_update_customer = True
            

            if mercately_points != str(odoo_points):
                payload["custom_fields"].append({
                "field_name": "puntos",
                "field_content": odoo_points
                })
                should_update_customer = True
            
            if should_update_customer:
                self.update_partner_points_and_referred_codes_in_mercately(mercately_partner_id,payload)
        else:
            print('El cliente con id: ', partner_id, ' de mercately no existe en el sistema Odoo')

    def _get_coupon_programs_from_partner_id(self, partner_id):
        coupon_programs = self.env['coupon.program'].search([
        ('program_type', '=', 'coupon_program'),
        ('active', '=', True),
        ('assigned_customer', '=', partner_id),
        ('coupon_type', '=', 'referred')
        ])

        coupon_ids = coupon_programs.read()[0]['coupon_ids']
        coupons = self.env['coupon.coupon'].search([('id', 'in', coupon_ids), ('state', '=', 'new')])
        coupon_data = coupons.read(['code'])
        coupon_codes = "\n".join([coupon['code'] for coupon in coupon_data])

        return coupon_codes