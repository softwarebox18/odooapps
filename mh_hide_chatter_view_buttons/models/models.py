# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools, _

class hide_chatter_view_buttons(models.Model):

    _name = 'hide.chatter.view.buttons'
    _description = 'Hide Chatter View and Button'
    _rec_name = 'user_id'

    user_id = fields.Many2one('res.users', string='Users')
    is_active = fields.Boolean(string="Active", default=True)
    hide_chatter_line_ids = fields.One2many('hide.chatter.view.buttons.lines','hide_chatter_id', string='Add Hide Info')

    # Apply the unique constraint in the user definition
    _sql_constraints = [
        ('user_id_unique',
         'UNIQUE (user_id)',
         'A configuration with this user already exists. Please use a different user.')
    ]

class hide_chatter_view_buttons_lines(models.Model):

    _name = 'hide.chatter.view.buttons.lines'

    model_id = fields.Many2one('ir.model', string='Model')
    model_name = fields.Char(related="model_id.model", store=True, readonly=True)
    hide_send_message = fields.Boolean(string="Hide Send Message", default=False)
    hide_log_note = fields.Boolean(string="Hide Log Note", default=False)
    hide_activities = fields.Boolean(string="Hide Activities", default=False)
    hide_file_upload = fields.Boolean(string="Hide File Upload", default=False)
    hide_mail_followers = fields.Boolean(string="Hide Mail Followers", default=False)
    hide_follow = fields.Boolean(string="Hide Follow", default=False)
    hide_chatter_id = fields.Many2one('hide.chatter.view.buttons', string='Hide Chatter Button', required=True, ondelete='cascade')

    # Apply the unique constraint in the model definition
    _sql_constraints = [
        (
            'unique_user_model',
            'unique(hide_chatter_id, model_id)',
            'A configuration with this user and model already exists.'
        )
    ]
    # _sql_constraints = [
    #     ('model_id_unique',
    #      'UNIQUE (model_id)',
    #      'A configuration with this model already exists. Please use a different model.')
    # ]
