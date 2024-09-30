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
        loyalty_points_model = self.env['loyalty.points']
        res_partner_model = self.env['res.partner']

        won_points = 0
        aux_points = 0
        spent_points = 0

        if operation == 'add':
            won_points = int(loyalty_points)
            aux_points = int(loyalty_points)
        if operation == 'substract':
            aux_points = int(loyalty_points) * -1
            spent_points = int(loyalty_points)
        try:
            args = {
                  'partner_id': partner_id,
                  'won_points': won_points,
                  'aux_points': aux_points,
                  'spent_points': spent_points,
                  'order_name': 'Orden de referido' 
                }
            
            loyalty_points_model.create(args)
            res_partner_model._compute_loyalty_points()
            _logger.info('Puntos modificados - Operacion exitosa')
            return [True, loyalty_points_model.get_points_for_partner(partner_id)]
        except Exception as e:
             _logger.error('Error al actualizar puntos: ',  e)
             return [False, loyalty_points_model.get_points_for_partner(partner_id)]
        
    def get_coupons_program_owner(self, program_id):
        coupon_program = self.env['coupon.program'].browse(program_id)
        coupon_program_data = coupon_program.read()[0]

        partner_id = coupon_program_data['assigned_customer'][0]
        partner = self.env['res.partner'].search([('id', '=', partner_id)], limit=1)
        return partner.read()
    
