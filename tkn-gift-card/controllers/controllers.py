# -*- coding: utf-8 -*-
# from odoo import http


# class Tkn-gift-card(http.Controller):
#     @http.route('/tkn-gift-card/tkn-gift-card', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tkn-gift-card/tkn-gift-card/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tkn-gift-card.listing', {
#             'root': '/tkn-gift-card/tkn-gift-card',
#             'objects': http.request.env['tkn-gift-card.tkn-gift-card'].search([]),
#         })

#     @http.route('/tkn-gift-card/tkn-gift-card/objects/<model("tkn-gift-card.tkn-gift-card"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tkn-gift-card.object', {
#             'object': obj
#         })
