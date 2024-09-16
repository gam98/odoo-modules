# -*- coding: utf-8 -*-

from odoo import models, api
import logging
import requests

_logger = logging.getLogger(__name__)

class PosOrder(models.Model):
    _inherit = "pos.order"

    def _process_order(self, order, draft, existing_order):

        # pylint: disable=no-member
        pos_order_id = super(PosOrder, self)._process_order(order, draft, existing_order)
        
        print('orderdata: ', order['data'])
        # TODO: restarle al partner original los puntos que se suman al dueño del programa
        # Notificar por whatsapp que se han sumado X puntos al tecnico correspondiente
        
        loyalty_points = order['data']['loyalty_points']
        booked_coupons = order['data']['bookedCouponCodes']
        first_coupon_data = next(iter(booked_coupons.values()))
        program_id = first_coupon_data.get('program_id')

        if program_id:
            coupon_program = self.env['coupon.program'].browse(program_id)
            coupon_program_data = coupon_program.read()[0]

            partner_id = coupon_program_data['assigned_customer'][0]
            points_added = self._add_points_to_program_owner(partner_id, loyalty_points)

            if points_added:
                return
                
        return pos_order_id

    
    def _substract_points_to_original_partner(self,partner_id, loyalty_points):
        return
    
    def _add_points_to_program_owner(self,partner_id,loyalty_points):
        partner = self.env['res.partner'].search([('id', '=', partner_id)], limit=1)
        partner_data = partner.read()

        current_loyalty_points = partner_data[0]['loyalty_points']
        new_loyalty_points = int(current_loyalty_points) + int(loyalty_points)
        name = partner_data[0]['name']

        try:
            partner.write({'loyalty_points': new_loyalty_points})
            _logger.info('Se han sumado %d puntos al cliente %s. Total puntos de lealtad: %d', new_loyalty_points, name, new_loyalty_points)
            return True
        except Exception as e:
             _logger.error('Error al cargar puntos para el cliente %s: %s', name, str(e))
             return False
        
    
