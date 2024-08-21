# -*- coding: utf-8 -*-
# from odoo import http


# class Tkn-reward-estimate(http.Controller):
#     @http.route('/tkn-reward-estimate/tkn-reward-estimate', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tkn-reward-estimate/tkn-reward-estimate/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tkn-reward-estimate.listing', {
#             'root': '/tkn-reward-estimate/tkn-reward-estimate',
#             'objects': http.request.env['tkn-reward-estimate.tkn-reward-estimate'].search([]),
#         })

#     @http.route('/tkn-reward-estimate/tkn-reward-estimate/objects/<model("tkn-reward-estimate.tkn-reward-estimate"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tkn-reward-estimate.object', {
#             'object': obj
#         })
