# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_allowed_companies = fields.Boolean("Allowed All Companies By Default",config_parameter='mh_all_company_select_unselect_dynamically.is_allowed_companies')

