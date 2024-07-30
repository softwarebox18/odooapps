# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Display Order Details in Sale Order List View',
    'summary': """Display Order Details in Sale Order List View""",
    'sequence': 901,
    'version': '17.0.1.0.0',
    'category': 'Sale',
    'author': 'Software Box',
    'website': 'http://softwarebox18@gmail.com',
    'price': '3.71',
    'currency': 'USD',
    'depends': ['base', 'sale'],
    'data': [
        'views/views.xml',
        # 'security/ir.model.access.csv',
    ],
    'images': ['static/description/main.PNG'],
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
