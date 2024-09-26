# -*- coding: utf-8 -*-

from odoo import models, api, fields, http
import requests
import logging

_logger = logging.getLogger(__name__)

class PosOrder(models.Model):
    _inherit = "pos.order"

    def _process_order(self, order, draft, existing_order):

        # pylint: disable=no-member
        pos_order_id = super(PosOrder, self)._process_order(order, draft, existing_order)
        loyalty_points = order['data']['loyalty_points']
        booked_coupons = order['data']['bookedCouponCodes']
        original_partner_id = order['data']['partner_id']
        try:
            first_coupon_data = next(iter(booked_coupons.values()))
        except:
            return pos_order_id
        program_id = first_coupon_data.get('program_id')

        if program_id:
            coupon_program = self.env['coupon.program'].browse(program_id)
            coupon_program_data = coupon_program.read()[0]

            partner_id = coupon_program_data['assigned_customer'][0]
            points_added = self._add_or_substract_points_to_program_owner(partner_id, loyalty_points,'add')

            if points_added[0]:
                self._add_or_substract_points_to_program_owner(original_partner_id, loyalty_points,'substract')

        return pos_order_id
    
    def _add_or_substract_points_to_program_owner(self,partner_id,loyalty_points,operation):
        partner = self.env['res.partner'].search([('id', '=', partner_id)], limit=1)
        partner_data = partner.read()
        current_loyalty_points = partner_data[0]['loyalty_points']

        if operation == 'add':
            new_loyalty_points = int(current_loyalty_points) + int(loyalty_points)
        if operation == 'substract':
            new_loyalty_points = int(current_loyalty_points) - int(loyalty_points)
        try:
            partner.write({'loyalty_points': new_loyalty_points})
            _logger.info('Puntos modificados - Operacion exitosa')
            return [True, new_loyalty_points]
        except Exception:
             _logger.error('Error al actualizar puntos')
             return [False, new_loyalty_points]
        
    def get_coupons_program_owner(self, program_id):
        coupon_program = self.env['coupon.program'].browse(program_id)
        coupon_program_data = coupon_program.read()[0]

        partner_id = coupon_program_data['assigned_customer'][0]
        partner = self.env['res.partner'].search([('id', '=', partner_id)], limit=1)
        return partner.read()
    
