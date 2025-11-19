# -*- coding: utf-8 -*-
{
    'name': "Moamalat LightBox Payment Gateway Integration",
    'summary': "Moamalat LightBox Payment Gateway Integration – Secure Online Payments",
    'description': """Moamalat LightBox Payment Gateway Integration – Secure Online Payments""",
    'sequence': -1,
    'version': '18.0.1.0.0',
    'author': "SoftwareBox",
    'website': "https://softwarebox18@gmail.com",
    'category': 'Accounting/Payment',
    'price': '290',
    'currency': 'EUR',
    'depends': ['payment'],
    'data': [
        'views/payment_form_templates.xml',
        'views/payment_provider_views.xml',
        'views/payment_transaction_views.xml',

        'data/payment_method_data.xml',
        'data/payment_provider_data.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'assets': {
        'web.assets_frontend': [
            'mh_moamalat_lightbox_payment/static/src/**/*',
        ],
    },
    'images': ['static/description/main.PNG'],
    'license': 'OPL-1',
}

