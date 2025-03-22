# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Dynamic Add Custom Filter Menu Visibility Hide/Unhide | Remove Add Custom Filter Menu | Disable Add Custom Filter Menu',
    'summary': """Dynamic Add Custom Filter Menu Visibility | Remove Add Custom Filter Menu | Disable Add Custom Filter Menu""",
    'sequence': -1,
    'version': '17.0.1.0.0',
    'category': 'Extra Tools',
    'author': 'Software Box',
    'website': 'http://softwarebox18@gmail.com',
    'module_type': 'industries',
    'price': '29.90',
    'currency': 'USD',
    'depends': ['base','web'],
    'data': [
        'security/groups.xml',
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'images': ['static/description/main.PNG'],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_frontend': [
        ],
        'web.assets_backend': [
            'mh_hide_add_custom_filter/static/src/filters/**/*',
        ],
    },
    'license': 'OPL-1',
}
