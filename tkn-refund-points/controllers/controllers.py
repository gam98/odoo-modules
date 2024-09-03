# -*- coding: utf-8 -*-
# from odoo import http


# class Tkn-refundPoints(http.Controller):
#     @http.route('/tkn-refund_points/tkn-refund_points', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tkn-refund_points/tkn-refund_points/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tkn-refund_points.listing', {
#             'root': '/tkn-refund_points/tkn-refund_points',
#             'objects': http.request.env['tkn-refund_points.tkn-refund_points'].search([]),
#         })

#     @http.route('/tkn-refund_points/tkn-refund_points/objects/<model("tkn-refund_points.tkn-refund_points"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tkn-refund_points.object', {
#             'object': obj
#         })
