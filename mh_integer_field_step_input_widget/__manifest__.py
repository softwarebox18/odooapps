# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Step Input Widget for Integer Fields',
    'summary': """Step Input Widget for Integer Fields""",
    'sequence': -1,
    'version': '16.0.1.0.0',
    'category': 'Web',
    'author': 'Software Box',
    'website': 'http://softwarebox18@gmail.com',
    'module_type': 'industries',
    'price': '4.90',
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
            'mh_integer_field_step_input_widget/static/src/views/fields/integer/integer_field_step_input_widget.css',
            'mh_integer_field_step_input_widget/static/src/views/fields/integer/integer_field_step_input_widget.xml',
            'mh_integer_field_step_input_widget/static/src/views/fields/integer/integer_field_step_input_widget.js',
            # 'mh_integer_field_step_input_widget/static/src/views/fields/**/*',
        ],
    },
    'license': 'OPL-1',
}
