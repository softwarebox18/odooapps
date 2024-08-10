# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Display Asterisk in Required Fields',
    'summary': """Display Asterisk in Required Fields""",
    'sequence': -1,
    'version': '15.0.1.0.0',
    'category': 'Extra Tools',
    'author': 'Software Box',
    'website': 'http://softwarebox18@gmail.com',
    'price': '6.00',
    'currency': 'USD',
    'depends': ['web'],
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
            # 'mh_display_asterisk_in_required_field/static/src/views/form/form_label_extend.css',
            # 'mh_display_asterisk_in_required_field/static/src/views/form/form_label_extend.xml',
            'mh_display_asterisk_in_required_field/static/src/views/**/*',
        ],
    },
    'license': 'OPL-1',
}
