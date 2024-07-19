# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools, _

class many2one_field_config(models.Model):

    _name = 'many2one.field.config'
    _description = 'Disable Quick Create'
    _rec_name = 'model_id'

    model_id = fields.Many2one('ir.model', string='Model')
    config_line_ids = fields.One2many('many2one.field.config.lines','config_id', string='Add Fields',ondelete='cascade')
    # fields_ids = fields.Many2many('ir.model.fields', string='Fields', domain="[('model_id', '=', model_id),('ttype', '=', 'many2one')]")

class add_search_limit_config_lines(models.Model):

    _name = 'many2one.field.config.lines'

    fields_id = fields.Many2one('ir.model.fields', string='Fields')
    is_hide_create_edit = fields.Boolean(string="Hide Create and Edit", default=False)
    search_limit = fields.Integer(string="Search Limit")
    quick_search_more_limit = fields.Integer(string="Quick Search More Limit", default=320)
    is_hide_search_more = fields.Boolean(string="Hide Search More", default=False)
    can_open = fields.Boolean(string="Can Open", default=True)
    config_id = fields.Many2one('many2one.field.config', string='Config', required=True)
