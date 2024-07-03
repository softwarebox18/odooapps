# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Product Barcode Generator',
    'summary': """Multi Products Dynamic Barcode Generator""",
    'description': """The Multi Products Barcode Generator module for Odoo empowers users to effortlessly generate and customize barcodes for products. Whether you’re managing inventory, tracking assets, or simplifying point-of-sale processes, this module provides the tools to streamline barcode generation within your Odoo environment.""",
    'sequence': -100,
    'version': '16.0.1.0.0',
    'category': 'Sale',
    'author': 'Mudassir Hassan',
    'website': 'http://mudassirh45@gmail.com',
    'module_type': 'industries',
    'price': '29.0',
    'currency': 'USD',
    'depends': ['base','purchase','product'],
    'data': [
        'security/security_access_data.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'images': ['static/description/main.png'],
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
