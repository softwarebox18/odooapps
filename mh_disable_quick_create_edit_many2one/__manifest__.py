# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Disable or Hide Quick Create and Edit Many2One Dynamically',
    'summary': """Disable or Hide Quick Create and Edit Many2One Dynamically""",
    'sequence': -1,
    'version': '17.0.1.0.0',
    'category': 'Website',
    'author': 'Mudassir Hassan',
    'website': 'http://mudassirh45@gmail.com',
    'module_type': 'industries',
    'price': '16.49',
    'currency': 'USD',
    'depends': ['base', 'web'],
    'data': [
        'views/views.xml',
        'security/ir.model.access.csv',
    ],
    'images': ['static/description/main.PNG'],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'mh_disable_quick_create_edit_many2one/static/src/js/disable_quick_create_edit.js',
        ],
    },
    'license': 'OPL-1',
}
