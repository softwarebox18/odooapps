# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Hide Powered By Odoo',
    'summary': """Hide Powered By Odoo and Manage Database""",
    'sequence': -1,
    'version': '15.0.1.0.0',
    'category': 'Website',
    'author': 'Mudassir Hassan',
    'website': 'http://mudassirh45@gmail.com',
    'module_type': 'industries',
    'price': '5.50',
    'currency': 'USD',
    'depends': ['base', 'web','website'],
    'data': [
        'views/views.xml',
        'views/custom_template.xml',
        # 'security/ir.model.access.csv',
    ],
    'images': ['static/description/main.PNG'],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_frontend': [
        ],
        'web.assets_backend': [
        ],
    },
    'license': 'OPL-1',
}
