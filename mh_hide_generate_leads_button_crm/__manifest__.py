# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Hide Generate Leads Button from CRM',
    'summary': """Hide Generate Leads Button from CRM""",
    'sequence': -1,
    'version': '16.0.1.0.0',
    'category': 'CRM',
    'author': 'Software Box',
    'website': 'http://softwarebox18@gmail.com',
    'module_type': 'industries',
    'price': '19.83',
    'currency': 'USD',
    'depends': ['crm','crm_iap_mine','web'],
    'data': [
        # 'views/views.xml',
        'security/groups.xml',
        # 'security/ir.model.access.csv',
    ],
    'images': ['static/description/main.PNG'],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'mh_hide_generate_leads_button_crm/static/src/views/**/*',
        ],
    },
    'license': 'OPL-1',
}
