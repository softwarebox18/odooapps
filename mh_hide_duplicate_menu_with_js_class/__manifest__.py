# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Hide & Show Duplicate Action Menu Dynamically with JS Class',
    'summary': """Hide & Show Duplicate Action Menu Dynamically with JS Class""",
    'sequence': -1,
    'version': '16.0.1.0.0',
    'category': 'Extra Tools',
    'author': 'Software Box',
    'website': 'http://softwarebox18@gmail.com',
    'module_type': 'industries',
    'price': '7.83',
    'currency': 'USD',
    'depends': ['base', 'web', 'sale'],
    'data': [
        'views/views.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
    ],
    'images': ['static/description/main.PNG'],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'mh_hide_duplicate_menu_with_js_class/static/src/views/**/*',
        ],
    },
    'license': 'OPL-1',
}
