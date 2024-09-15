# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Dynamic Many2One Field Options',
    'summary': """Dynamic Many2One Field Options""",
    'sequence': -1,
    'version': '16.0.1.0.0',
    'category': 'Extra Tools',
    'author': 'Software Box',
    'website': 'http://softwarebox18@gmail.com',
    'module_type': 'industries',
    'price': '46.69',
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
            'mh_dynamic_many2one_field_options/static/src/js/dynamic_many2one_field_options.js',
        ],
    },
    'license': 'OPL-1',
}
