# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_allowed_companies = fields.Boolean(
        'Allowed All Companies By Default',
        help="Select/Unselect All Companies By Default",
        config_parameter='mh_all_company_select_unselect_dynamically.is_allowed_companies', default=False)

    # @api.model
    # def get_values(self):
    #     res = super(ResConfigSettings, self).get_values()
    #
    #     res['is_allowed_companies'] = self.env['ir.config_parameter'].sudo().get_param('mh_all_company_select_unselect_dynamically.is_allowed_companies', default=False)
    #
    #     return res
    #
    # @api.model
    # def set_values(self):
    #     self.env['ir.config_parameter'].sudo().set_param('mh_all_company_select_unselect_dynamically.is_allowed_companies', self.is_allowed_companies)
    #
    #     super(ResConfigSettings, self).set_values()


