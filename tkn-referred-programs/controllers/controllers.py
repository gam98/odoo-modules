# -*- coding: utf-8 -*-
# from odoo import http


# class Tkn-referred-programs(http.Controller):
#     @http.route('/tkn-referred-programs/tkn-referred-programs', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tkn-referred-programs/tkn-referred-programs/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tkn-referred-programs.listing', {
#             'root': '/tkn-referred-programs/tkn-referred-programs',
#             'objects': http.request.env['tkn-referred-programs.tkn-referred-programs'].search([]),
#         })

#     @http.route('/tkn-referred-programs/tkn-referred-programs/objects/<model("tkn-referred-programs.tkn-referred-programs"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tkn-referred-programs.object', {
#             'object': obj
#         })
