# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Dynamic Multi-Field Name Search for Many2One Fields',
    'summary': """Dynamic Multi-Field Name Search for Many2One Fields""",
    'sequence': -1,
    'version': '17.0.1.0.0',
    'category': 'Extra Tools',
    'author': 'Software Box',
    'website': 'http://softwarebox18@gmail.com',
    'module_type': 'industries',
    'price': '39.36',
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
            'mh_dynamic_name_search/static/src/js/dynamic_name_search.js',
        ],
    },
    'license': 'OPL-1',
}
