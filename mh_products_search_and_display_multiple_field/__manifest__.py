# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Search and Display Multiple Fields on Product Many2one Field in Odoo',
    'summary': """Search and Display Multiple Fields on Product Many2one (Quotation, SO, PO and MO etc) Field in Odoo""",
    'sequence': -1,
    'version': '18.0.1.0.0',
    'category': 'Discuss',
    'author': 'Software Box',
    'website': 'http://softwarebox18@gmail.com',
    'price': '9.99',
    'currency': 'USD',
    'depends': ['base', 'product', 'sale'],
    'data': [
        'views/views.xml',
        # 'security/ir.model.access.csv',
    ],
    'images': ['static/description/main.PNG'],
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
