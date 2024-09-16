# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools, _

class many2one_field_change_label_config(models.Model):

    _name = 'many2one.field.change.label.config'
    _description = 'Dynamic Many2One Field Label Customizer'
    _rec_name = 'model_id'

    model_id = fields.Many2one('ir.model', string='Model')
    is_active = fields.Boolean(string="Active", default=False)
    config_line_ids = fields.One2many('many2one.field.change.label.config.lines','config_id', string='Add Fields', required=True)

    # Apply the unique constraint in the model definition
    _sql_constraints = [
        ('model_id_unique',
         'UNIQUE (model_id)',
         'A configuration with this model already exists. Please use a different model.')
    ]

class many2one_field_change_label_config_lines(models.Model):

    _name = 'many2one.field.change.label.config.lines'

    fields_id = fields.Many2one('ir.model.fields', string='Fields')
    create_label = fields.Char(string="Create", default="Create")
    create_and_edit = fields.Char(string="Create and Edit...", default="Create and Edit...")
    search_more_label = fields.Char(string="Search More...", default="Search More...")
    start_typing_label = fields.Char(string="Start typing...", default="Start typing...")
    no_record_label = fields.Char(string="No records", default="No records")

    config_id = fields.Many2one('many2one.field.change.label.config', string='Config', required=True, ondelete='cascade')
