# -*- coding: utf-8 -*-
# from odoo import http


# class SdCustomSale(http.Controller):
#     @http.route('/sd_custom_sale/sd_custom_sale', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sd_custom_sale/sd_custom_sale/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sd_custom_sale.listing', {
#             'root': '/sd_custom_sale/sd_custom_sale',
#             'objects': http.request.env['sd_custom_sale.sd_custom_sale'].search([]),
#         })

#     @http.route('/sd_custom_sale/sd_custom_sale/objects/<model("sd_custom_sale.sd_custom_sale"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sd_custom_sale.object', {
#             'object': obj
#         })

