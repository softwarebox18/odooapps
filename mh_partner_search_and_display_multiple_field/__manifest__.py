# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Search and Display Multiple Values on Partner/Customer/Vendor Many2one Field',
    'summary': """Search and Display Multiple Values on Partner/Customer/Vendor Many2one Field""",
    'sequence': -1,
    'version': '17.0.1.0.0',
    'category': 'Discuss',
    'author': 'Software Box',
    'website': 'http://softwarebox18@gmail.com',
    'price': '9.99',
    'currency': 'USD',
    'depends': ['base', 'mail'],
    'data': [
        'views/views.xml',
        # 'security/ir.model.access.csv',
    ],
    'images': ['static/description/main.PNG'],
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
