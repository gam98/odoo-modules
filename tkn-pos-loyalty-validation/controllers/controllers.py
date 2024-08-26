# -*- coding: utf-8 -*-
# from odoo import http


# class Tkn-pos-loyalty-validation(http.Controller):
#     @http.route('/tkn-pos-loyalty-validation/tkn-pos-loyalty-validation', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tkn-pos-loyalty-validation/tkn-pos-loyalty-validation/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tkn-pos-loyalty-validation.listing', {
#             'root': '/tkn-pos-loyalty-validation/tkn-pos-loyalty-validation',
#             'objects': http.request.env['tkn-pos-loyalty-validation.tkn-pos-loyalty-validation'].search([]),
#         })

#     @http.route('/tkn-pos-loyalty-validation/tkn-pos-loyalty-validation/objects/<model("tkn-pos-loyalty-validation.tkn-pos-loyalty-validation"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tkn-pos-loyalty-validation.object', {
#             'object': obj
#         })
