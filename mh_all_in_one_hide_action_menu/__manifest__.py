# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Hide Delete | Duplicate | Export | Export All | Archive | Unarchive Action Menu Button Dynamically',
    'summary': """Hide Delete | Duplicate | Export | Export All | Archive | Unarchive Action Menu Button Dynamically""",
    'sequence': -1,
    'version': '16.0.1.0.0',
    'category': 'Extra Tools',
    'author': 'Software Box',
    'website': 'http://softwarebox18@gmail.com',
    'module_type': 'industries',
    'price': '7.83',
    'currency': 'USD',
    'depends': ['base', 'web'],
    'data': [
        'views/views.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
    ],
    'images': ['static/description/main.PNG'],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'mh_all_in_one_hide_action_menu/static/src/views/**/*',
        ],
    },
    'license': 'OPL-1',
}
