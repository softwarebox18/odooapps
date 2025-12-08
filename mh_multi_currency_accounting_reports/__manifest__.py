# -*- coding: utf-8 -*-
{
    "name": "Multi-Currency Accounting Reports",
    "summary": "Improve your accounting reporting with full multi-currency support in Odoo 18. This module ensures that the Amount Currency column always displays the original transaction currency, while other report columns convert dynamically to the selected reporting currency. Works for Aged Receivable, Aged Payable, and Partner Ledger reports.",
    'sequence': -1,
    'version': '18.0.1.0.0',
    'category': 'Accounting',
    'author': 'Software Box',
    'website': 'http://softwarebox18@gmail.com',
    "license": "LGPL-3",
    'price': '69',
    'currency': 'EUR',
    "description": """Improve your accounting reporting with full multi-currency support in Odoo 18. This module ensures that the Amount Currency column always displays the original transaction currency, while other report columns convert dynamically to the selected reporting currency. Works for Aged Receivable, Aged Payable, and Partner Ledger reports.""",
    "depends": ["account_reports"],
    "data": [
        'views/views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'mh_multi_currency_accounting_reports/static/src/components/**/*',
        ],
    },
    "application": True,
    "installable": True,
    'images': ['static/description/main.PNG'],
}
