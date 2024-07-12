# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools, _

class disable_quick_create_edit_config(models.Model):

    _name = 'disable.quick.create.edit.config'
    _description = 'Disable Quick Create'
    _rec_name = 'model_id'

    model_id = fields.Many2one('ir.model', string='Model')
    fields_ids = fields.Many2many('ir.model.fields', string='Fields', domain="[('model_id', '=', model_id),('ttype', '=', 'many2one')]")
