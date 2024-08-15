# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Hide & Show Delete Action Menu Button Dynamically',
    'summary': """Hide & Show Delete Action Menu Button Dynamically""",
    'sequence': -1,
    'version': '17.0.1.0.0',
    'category': 'Extra Tools',
    'author': 'Software Box',
    'website': 'http://softwarebox18@gmail.com',
    'module_type': 'industries',
    'price': '7.36',
    'currency': 'USD',
    'depends': ['base', 'web'],
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
            'mh_hide_delete_button_dynamically/static/src/views/**/*',
        ],
    },
    'license': 'OPL-1',
}
