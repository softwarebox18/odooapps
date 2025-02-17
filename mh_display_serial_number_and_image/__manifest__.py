# -*- coding: utf-8 -*-
{
    'name': 'Display Serial Number and Image in Sale Order Line and Report',
    'summary': """Display Serial Number and Image in Sale Order Line and Report""",
    'sequence': -1,
    'version': '18.0.1.0.0',
    'category': 'Sale',
    'author': 'Software Box',
    'website': 'http://softwarebox18@gmail.com',
    'module_type': 'industries',
    'price': '8.90',
    'currency': 'USD',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        'security/group.xml',
        # 'security/ir.model.access.csv',
        'report/ir_actions_report.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

