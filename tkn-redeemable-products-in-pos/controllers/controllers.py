# -*- coding: utf-8 -*-
# from odoo import http


# class Tkn-redeemable-products-in-pos(http.Controller):
#     @http.route('/tkn-redeemable-products-in-pos/tkn-redeemable-products-in-pos', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tkn-redeemable-products-in-pos/tkn-redeemable-products-in-pos/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tkn-redeemable-products-in-pos.listing', {
#             'root': '/tkn-redeemable-products-in-pos/tkn-redeemable-products-in-pos',
#             'objects': http.request.env['tkn-redeemable-products-in-pos.tkn-redeemable-products-in-pos'].search([]),
#         })

#     @http.route('/tkn-redeemable-products-in-pos/tkn-redeemable-products-in-pos/objects/<model("tkn-redeemable-products-in-pos.tkn-redeemable-products-in-pos"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tkn-redeemable-products-in-pos.object', {
#             'object': obj
#         })
