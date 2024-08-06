# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Display Cost Price in SO Pivot Report",
    'summary': 'Display Cost Price in SO Pivot Report',
    'version': '17.0.1.0.0',
    'sequence': -1,
    'description': """
        Display Cost Price in SO Pivot Report
    """,
    'category': "Sale",
    'author': 'Software Box',
    'website': 'http://softwarebox18@gmail.com',
    'price': '5.75',
    'currency': 'USD',

    'depends': ['sale'],

    'data': [
        # 'views/sale_order_view.xml',
        'views/sale_order_report_view.xml',
    ],
    'images': ['static/description/main.PNG'],
    'installable': True,
    'auto_install': True,
    'license': 'LGPL-3',
}
