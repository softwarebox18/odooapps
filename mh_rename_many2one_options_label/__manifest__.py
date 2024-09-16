# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Dynamic Many2One Field Options Label Customizer',
    'summary': """Dynamic Many2One Field Options Label Customizer""",
    'sequence': -1,
    'version': '17.0.1.0.0',
    'category': 'Website',
    'author': 'Software Box',
    'website': 'http://softwarebox18@gmail.com',
    'module_type': 'industries',
    'price': '47.90',
    'currency': 'USD',
    'depends': ['base','web'],
    'data': [
        'views/views.xml',
        'security/ir.model.access.csv',
    ],
    'images': ['static/description/main.PNG'],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_frontend': [
        ],
        'web.assets_backend': [
            'mh_rename_many2one_options_label/static/src/js/change_label_many2one.js',
        ],
    },
    'license': 'OPL-1',
}
