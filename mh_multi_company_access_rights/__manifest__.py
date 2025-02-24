# -*- coding: utf-8 -*-
{
    'name': 'Multi-Company User Group & Menu Access Manager',
    'summary': """Multi-Company Access Rights | Multi-Company User Group & Menu Access Manager | Manage Different User Access Rights and Menus Visibility for each Company""",
    'sequence': -1,
    'version': '15.0.1.0.0',
    'category': 'Extra Tools',
    'author': 'Software Box',
    'website': 'http://softwarebox18@gmail.com',
    'module_type': 'industries',
    'price': '170.00',
    'currency': 'USD',

    # any module necessary for this one to work correctly
    'depends': ['base','web'],

    # always loaded
    'data': [
        # 'security/group.xml',
        'security/ir.model.access.csv',
        # 'report/ir_actions_report.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    'images': ['static/description/main.PNG'],
    'installable': True,
    'application': True,
    'assets': {
            'web.assets_frontend': [
            ],
            'web.assets_backend': [
                'mh_multi_company_access_rights/static/src/webclient/**/*',
            ],
        },
    'license': 'OPL-1',
}

