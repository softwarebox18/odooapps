# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Select/Unselect All Companies from Multi-company',
    'summary': """Select/Unselect All Companies from Multi-company""",
    'sequence': -1,
    'version': '17.0.1.0.0',
    'category': 'Website',
    'author': 'Mudassir Hassan',
    'website': 'http://mudassirh45@gmail.com',
    'module_type': 'industries',
    'price': '7.90',
    'currency': 'USD',
    'depends': ['base','web'],
    'data': [
        'views/views.xml',
        # 'security/ir.model.access.csv',
    ],
    'images': ['static/description/main.PNG'],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_frontend': [
        ],
        'web.assets_backend': [
            'mh_all_company_select_unselect/static/src/webclient/**/*',
        ],
    },
    'license': 'OPL-1',
}
