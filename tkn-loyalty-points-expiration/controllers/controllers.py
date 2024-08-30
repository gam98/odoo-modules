# -*- coding: utf-8 -*-
# from odoo import http


# class Tkn-loyalty-points-expiration(http.Controller):
#     @http.route('/tkn-loyalty-points-expiration/tkn-loyalty-points-expiration', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tkn-loyalty-points-expiration/tkn-loyalty-points-expiration/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tkn-loyalty-points-expiration.listing', {
#             'root': '/tkn-loyalty-points-expiration/tkn-loyalty-points-expiration',
#             'objects': http.request.env['tkn-loyalty-points-expiration.tkn-loyalty-points-expiration'].search([]),
#         })

#     @http.route('/tkn-loyalty-points-expiration/tkn-loyalty-points-expiration/objects/<model("tkn-loyalty-points-expiration.tkn-loyalty-points-expiration"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tkn-loyalty-points-expiration.object', {
#             'object': obj
#         })
