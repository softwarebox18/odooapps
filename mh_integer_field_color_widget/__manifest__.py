# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Dynamic Color-Changing Integer Field Widget Based on Threshold Value',
    'summary': """Dynamic Color-Changing Integer Field Widget Based on Threshold Value""",
    'sequence': -1,
    'version': '16.0.1.0.0',
    'category': 'Web',
    'author': 'Software Box',
    'website': 'http://softwarebox18@gmail.com',
    'module_type': 'industries',
    'price': '16.90',
    'currency': 'USD',
    'depends': ['base','web','hr'],
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
            'mh_integer_field_color_widget/static/src/views/fields/integer/integer_field_color_widget.css',
            'mh_integer_field_color_widget/static/src/views/fields/integer/integer_field_color_widget.xml',
            'mh_integer_field_color_widget/static/src/views/fields/integer/integer_field_color_widget.js',
            # 'mh_integer_field_color_widget/static/src/views/fields/**/*',
        ],
    },
    'license': 'OPL-1',
}
