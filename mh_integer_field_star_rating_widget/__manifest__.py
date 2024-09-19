# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Star Rating Dynamic Widget',
    'summary': """Star Rating Dynamic Widget""",
    'sequence': -1,
    'version': '17.0.1.0.0',
    'category': 'Web',
    'author': 'Software Box',
    'website': 'http://softwarebox18@gmail.com',
    'module_type': 'industries',
    'price': '39.78',
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
            'mh_integer_field_star_rating_widget/static/src/views/fields/integer/integer_field_star_rating_widget.css',
            'mh_integer_field_star_rating_widget/static/src/views/fields/integer/integer_field_star_rating_widget.xml',
            'mh_integer_field_star_rating_widget/static/src/views/fields/integer/integer_field_star_rating_widget.js',
            # 'mh_integer_field_star_rating_widget/static/src/views/fields/**/*',
        ],
    },
    'license': 'OPL-1',
}
