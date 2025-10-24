# -*- coding: utf-8 -*-
{
    'name': "Salesman User Group and Access Control",
    'summary': "Salesman User Group and Access Control Base Module",
    'description': """Salesman User Group and Access Control Base Module""",
    'sequence': -1,
    'version': '18.0.1.0.0',
    'category': "Base",
    'author': 'Software Box',
    'website': 'http://softwarebox18@gmail.com',
    'price': '5',
    'currency': 'EUR',
    'module_type': 'industries',
    'depends': ['base','sale_management','product','stock','account','uom','mail',],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'images': [
        'static/description/main.PNG'
    ],
    'license': 'OPL-1',
    'installable': True,
    'application': True,
}

