# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Hide Chatter View Buttons Dynamically',
    'summary': """Hide Chatter View Buttons Dynamically""",
    'sequence': -1,
    'version': '18.0.1.0.0',
    'category': 'Discuss',
    'author': 'Software Box',
    'website': 'http://softwarebox18@gmail.com',
    'module_type': 'industries',
    'price': '34.80',
    'currency': 'USD',
    'depends': ['mail'],
    'data': [
        'views/views.xml',
        'security/ir.model.access.csv',
    ],
    'images': ['static/description/main.PNG'],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'mh_hide_chatter_view_buttons/static/src/xml/hide_chatter_view_buttons.xml',
            'mh_hide_chatter_view_buttons/static/src/js/hide_chatter_view_buttons.js',
        ],
    },
    'license': 'OPL-1',
}
