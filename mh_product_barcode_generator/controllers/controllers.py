# -*- coding: utf-8 -*-
# from odoo import http


# class DmsBarcode(http.Controller):
#     @http.route('/mh_product_barcode_generator/mh_product_barcode_generator', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mh_product_barcode_generator/mh_product_barcode_generator/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mh_product_barcode_generator.listing', {
#             'root': '/mh_product_barcode_generator/mh_product_barcode_generator',
#             'objects': http.request.env['mh_product_barcode_generator.mh_product_barcode_generator'].search([]),
#         })

#     @http.route('/mh_product_barcode_generator/mh_product_barcode_generator/objects/<model("mh_product_barcode_generator.mh_product_barcode_generator"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mh_product_barcode_generator.object', {
#             'object': obj
#         })
