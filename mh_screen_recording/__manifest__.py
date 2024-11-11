# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Employee Monitoring | Screen Recording in Odoo",
    'summary': """Employee Monitoring | Screen Recording in Odoo""",
    'sequence': -1,
    'version': '16.0.1.0.0',
    'category': "Extra Tools",
    'author': 'Software Box',
    'website': 'http://softwarebox18@gmail.com',
    'price': '480.49',
    'currency': 'USD',
    'module_type': 'industries',

    'depends': ['base','hr', 'hr_attendance','hr_timesheet'],
    'data': [
        'security/ir.model.access.csv',
        'views/screen_recording_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
          # "mh_screen_recording/static/src/js/button_systray.js",
            "mh_screen_recording/static/src/xml/video_preview_widget.xml",
            "mh_screen_recording/static/src/xml/screen_recording_systray.xml",
            "mh_screen_recording/static/src/js/video_preview_widget.js"
        ],
        'web.assets_common': [
            "mh_screen_recording/static/src/js/screen_recording_systray.js",
            # "mh_screen_recording/static/src/xml/button_systray.xml",
        ],
    },
    'images': [
        'static/description/main.PNG'
    ],
    'license': 'OPL-1',
    'installable': True,
    'application': True,
}
