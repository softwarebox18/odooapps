# -*- coding: utf-8 -*-
{
    'name': "Restrict Transfers with Insufficient Stock",
    'summary': "Blocks validation of internal transfers and delivery orders when available quantity is less than the ordered quantity.",
    'description': """Blocks validation of internal transfers and delivery orders when available quantity is less than the ordered quantity.""",
    'sequence': -1,
    'version': '18.0.1.0.0',
    'category': "Stock",
    'author': 'Software Box',
    'website': 'http://softwarebox18@gmail.com',
    'price': '25',
    'currency': 'EUR',
    'module_type': 'industries',
    'depends': ['base','mh_salesman_group','stock'],
    'data': [
        # 'security/security.xml',
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'images': [
        'static/description/main.PNG'
    ],
    'license': 'OPL-1',
    'installable': True,
    'application': True,
}

