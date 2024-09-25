# -*- coding: utf-8 -*-
# from odoo import http


# class Tkn-mercately-integration(http.Controller):
#     @http.route('/tkn-mercately-integration/tkn-mercately-integration', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tkn-mercately-integration/tkn-mercately-integration/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tkn-mercately-integration.listing', {
#             'root': '/tkn-mercately-integration/tkn-mercately-integration',
#             'objects': http.request.env['tkn-mercately-integration.tkn-mercately-integration'].search([]),
#         })

#     @http.route('/tkn-mercately-integration/tkn-mercately-integration/objects/<model("tkn-mercately-integration.tkn-mercately-integration"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tkn-mercately-integration.object', {
#             'object': obj
#         })
