# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Set Text, Image and PDF Watermark in QWEB PDF Report",
    'summary': """Set Text, Image and PDF Watermark in QWEB PDF Report""",
    'sequence': -1,
    'version': '18.0.1.0.0',
    'category': "Tools",
    'author': 'Software Box',
    'website': 'http://softwarebox18@gmail.com',
    'price': '68.49',
    'currency': 'EUR',
    'module_type': 'industries',

    'depends': ['base','base_setup'],
    "external_dependencies": {"python": ["PyPDF2"]},
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'assets': {
        # 'web.assets_backend': [
        # ],
    },
    'images': [
        'static/description/main.PNG'
    ],
    'license': 'OPL-1',
    'installable': True,
    'application': True,
}
