# -*- coding: utf-8 -*-
# from odoo import http


# class Tkn-redeemable-products-bulk-loader(http.Controller):
#     @http.route('/tkn-redeemable-products-bulk-loader/tkn-redeemable-products-bulk-loader', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tkn-redeemable-products-bulk-loader/tkn-redeemable-products-bulk-loader/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tkn-redeemable-products-bulk-loader.listing', {
#             'root': '/tkn-redeemable-products-bulk-loader/tkn-redeemable-products-bulk-loader',
#             'objects': http.request.env['tkn-redeemable-products-bulk-loader.tkn-redeemable-products-bulk-loader'].search([]),
#         })

#     @http.route('/tkn-redeemable-products-bulk-loader/tkn-redeemable-products-bulk-loader/objects/<model("tkn-redeemable-products-bulk-loader.tkn-redeemable-products-bulk-loader"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tkn-redeemable-products-bulk-loader.object', {
#             'object': obj
#         })
