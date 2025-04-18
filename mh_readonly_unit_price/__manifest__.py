# -*- coding: utf-8 -*-
{
    'name': 'Readonly Unit Price in Product, Sale Order Lines and Invoice Lines',
    'summary': """Readonly Unit Price in Product, Sale Order Lines and Invoice Lines""",
    'sequence': -1,
    'version': '18.0.1.0.0',
    'category': 'Sale',
    'author': 'Software Box',
    'website': 'http://softwarebox18@gmail.com',
    'price': '4.90',
    'currency': 'USD',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'sale', 'account'],

    # always loaded
    'data': [
        'security/group.xml',
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'images': ['static/description/main.PNG'],
    'installable': True,
    'application': True,

    'license': 'OPL-1',
}

