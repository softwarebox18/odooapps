# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Multi Company Favicon',
    'summary': """Multi Company Favicon - Configuring a favicon for each company in Odoo 17 is currently not feasible. However, it can be done for the website. We offer a solution for you to set up your own favicon in the backend. Simply navigate to the company settings, update the favicon image, and you're all set.""",
    'sequence': -100,
    'version': '17.0.1.0.0',
    'category': 'Website',
    'author': 'Mudassir Hassan',
    'website': 'http://mudassirh45@gmail.com',
    'module_type': 'industries',
    'price': '1.0',
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
