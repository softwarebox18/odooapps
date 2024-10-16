# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Multi Company Favicon',
    'summary': """Multi Company Favicon""",
    'sequence': -1,
    'version': '18.0.1.0.0',
    'category': 'Website',
    'author': 'Software Box',
    'website': 'http://softwarebox18@gmail.com',
    'module_type': 'industries',
    'price': '0.97',
    'currency': 'USD',
    'depends': ['base', 'web'],
    'data': [
        'views/views.xml',
        'views/custom_favicon_template.xml',
        # 'security/ir.model.access.csv',
    ],
    'images': ['static/description/main.PNG'],
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
