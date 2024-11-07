# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    enable_recording = fields.Boolean(
        string='Enable Recording',
        config_parameter='mh_screen_recording.enable_recording',
        help="Enable or disable screen recording functionality."
    )

    recording_check_interval = fields.Integer(
        string='Recording Check Interval (in Minutes)',
        config_parameter='mh_screen_recording.recording_check_interval',
        help="Set the interval (in minutes) for checking attendance status and scheduling screen recording."
    )

    recording_min_delay = fields.Integer(
        string='Minimum Recording Delay (in Minutes)',
        config_parameter='mh_screen_recording.recording_min_delay',
        help="Set the minimum delay time (in minutes) before starting a recording."
    )

    recording_max_delay = fields.Integer(
        string='Maximum Recording Delay (in Minutes)',
        config_parameter='mh_screen_recording.recording_max_delay',
        help="Set the maximum delay time (in minutes) before starting a recording."
    )

    recording_duration = fields.Integer(
        string='Recording Duration (In Seconds)',
        readonly=False,
        config_parameter='mh_screen_recording.recording_duration',
        help="Set the duration of video recordings in seconds."
    )

    screen_sharing_timeout = fields.Integer(
        string='Screen Sharing Timeout (In Seconds)',
        readonly=False,
        config_parameter='mh_screen_recording.screen_sharing_timeout',
        help="Set screen sharing timeout in seconds."
    )


class HrAttendanceInherit(models.Model):
    _inherit = 'hr.attendance'

    attendance_date = fields.Date(
        string="Attendance Date",
        default=lambda self: datetime.today().date(),
        help="The date when the attendance was marked."
    )

    @api.model
    def get_employee_attendance_status(self, user_id):
        # Get the employee associated with the current user
        employee = self.env['hr.employee'].search([('user_id', '=', user_id)], limit=1)
        if not employee:
            return {'is_checked_in': False, 'is_checked_out': False}

        # Get the latest attendance record for this employee
        today = datetime.today().date()
        # attendance = self.search([('employee_id', '=', employee.id), ('check_in', '>=', today)], order='check_in desc', limit=1)
        attendance = self.search([('employee_id', '=', employee.id), ('attendance_date', '=', today)], order='check_in desc', limit=1)
        print('111111111111111',today,attendance.check_in)
        # Check if the employee is currently checked in or checked out
        if attendance:
            is_checked_in = bool(attendance.check_in and not attendance.check_out)
            is_checked_out = bool(attendance.check_out)  # True if there's a checkout time
            return {
                'is_checked_in': is_checked_in,
                'is_checked_out': is_checked_out,
            }
        else:
            return {'is_checked_in': False, 'is_checked_out': False}

class ScreenRecording(models.Model):
    _name = 'screen.recording'
    _description = 'Screen Recording for Timesheets'
    _rec_name = 'user_id'

    user_id = fields.Many2one('res.users', string="User",default=lambda self: self.env.user.id)
    video_url = fields.Char(string="Video URL")
    duration = fields.Float("Duration (in seconds)")
    recorded_at = fields.Datetime("Recorded At", default=fields.Datetime.now)
    failed_attempts = fields.Integer(string="Failed Attempts", default=0)  # Add this field
    status = fields.Selection([('Screen Shared', 'Screen Shared'), ('Screen Not Shared', 'Screen Not Shared')], string="Status")

    @api.model
    def video_record(self, url, duration):
        """Function used to create a record when the screen record is
         stopped"""
        self.create({'video_url': url,'status': 'Screen Shared', 'duration': duration})
        return True

    @api.model
    def log_failed_attempt(self):
        """Log a failed screen recording attempt for the user on the current date."""
        today = datetime.today().date()

        # Search for an existing record for the user with today's date
        record = self.search([
            ('status', '=', 'Screen Not Shared'),
            ('user_id', '=', self.env.user.id),
            ('recorded_at', '>=', datetime.combine(today, datetime.min.time())),
            ('recorded_at', '<=', datetime.combine(today, datetime.max.time()))
        ], limit=1)

        if record:
            # Increment the failed_attempts counter if a record exists for today
            record.failed_attempts += 1
        else:
            # Create a new record if none exists for today
            self.create({
                'status': 'Screen Not Shared',
                'user_id': self.env.user.id,
                'failed_attempts': 1,
                'recorded_at': fields.Datetime.now(),  # Set to current timestamp
            })

        return True


