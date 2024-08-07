# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools, _

class hide_duplicate_button_config(models.Model):

    _name = 'hide.duplicate.button.config'
    _description = 'Hide Duplicate Action Menu Button'
    _rec_name = 'model_id'

    model_id = fields.Many2one('ir.model', string='Model')
    is_active = fields.Boolean(string="Active", default=False)

    # Apply the unique constraint in the model definition
    _sql_constraints = [
        ('model_id_unique',
         'UNIQUE (model_id)',
         'A configuration with this model already exists. Please use a different model.')
    ]

