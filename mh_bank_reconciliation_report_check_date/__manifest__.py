# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Bank Reconciliation Report Check Date and Filter',
    'summary': """Bank Reconciliation Report Check Date and Filter""",
    'sequence': -1,
    'version': '18.0.1.0.0',
    'category': 'Accounting',
    'author': 'Software Box',
    'website': 'http://softwarebox18@gmail.com',
    'price': '40',
    'currency': 'EUR',
    'depends': ['base', 'account', 'account_reports'],
    'data': [
        'views/views.xml',
        'security/ir.model.access.csv',
    ],
    'assets': {
       'web.assets_backend': [
           'mh_bank_reconciliation_report_check_date/static/src/components/**/*',
       ],
    },
    'images': ['static/description/main.PNG'],
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
