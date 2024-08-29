# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Display Sales Person Filter on Partner Ledger',
    'summary': """Display  Sales Person Filter on Partner Ledger""",
    'sequence': -1,
    'version': '17.0.1.0.0',
    'category': 'Accounting',
    'author': 'Software Box',
    'website': 'http://softwarebox18@gmail.com',
    'price': '49.71',
    'currency': 'USD',
    'depends': ['base', 'account','account_reports'],
    'data': [
        'views/views.xml',
        # 'security/ir.model.access.csv',
    ],
    'assets': {
        'web.assets_backend': [
            'mh_sales_person_filter_partner_ledger/static/src/components/**/*',
            # 'mh_sales_person_filter_partner_ledger/static/src/js/**/*',
        ],
    },
    'images': ['static/description/main.PNG'],
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
