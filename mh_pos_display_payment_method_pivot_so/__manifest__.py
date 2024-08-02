# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "POS Display Payment Method in SO Pivot Report",
    'summary': 'POS Display Payment Method in SO Pivot Report',
    'version': '17.0.1.0.0',
    'sequence': -1,
    'description': """
        POS Display Payment Method in SO Pivot Report
    """,
    'category': "Point of Sale",
    'author': 'Software Box',
    'website': 'http://softwarebox18@gmail.com',
    'price': '4.00',
    'currency': 'USD',

    'depends': ['point_of_sale'],

    'data': [
        # 'views/pos_order_view.xml',
        'views/pos_order_report_view.xml',
    ],
    'installable': True,
    'auto_install': True,
    'license': 'LGPL-3',
}
