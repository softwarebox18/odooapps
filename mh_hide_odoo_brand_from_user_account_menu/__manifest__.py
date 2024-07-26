# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Hide Documentation,Support,Shortcut Menu',
    'summary': """Hide Documentation,Support,Shortcut Menu""",
    'sequence': -1,
    'version': '17.0.1.0.0',
    'category': 'Extra Tools',
    'author': 'Software Box',
    'website': 'http://softwarebox18@gmail.com',
    'module_type': 'industries',
    'price': '4.80',
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
            'mh_hide_odoo_brand_from_user_account_menu/static/src/js/remove_specific_menu.js',
        ],
    },
    'license': 'OPL-1',
}
