# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Multi-Company Auto Selection – Default & All Companies Toggle for Odoo',
    'summary': """Multi-Company Auto Selection – Default & All Companies Toggle for Odoo""",
    'sequence': -1,
    'version': '16.0.1.0.0',
    'category': 'Website',
    'author': 'Software Box',
    'website': 'http://softwarebox18@gmail.com',
    'module_type': 'industries',
    'price': '7.90',
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
            'mh_all_company_select_unselect_dynamically/static/src/webclient/**/*',
        ],
    },
    'license': 'OPL-1',
}
