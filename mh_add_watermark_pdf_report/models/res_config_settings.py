# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):

    _inherit = ["res.config.settings"]

    watermark_type = fields.Selection(related='company_id.watermark_type', readonly=False)
    watermark_text = fields.Char(related='company_id.watermark_text', readonly=False)
    font_name = fields.Selection(related='company_id.font_name', readonly=False)
    font_size = fields.Integer(related='company_id.font_size', readonly=False)
    font_color = fields.Selection(related='company_id.font_color', readonly=False)
    opacity = fields.Integer(related='company_id.opacity', readonly=False)
    rotation = fields.Integer(related='company_id.rotation', readonly=False)
    scale_factor = fields.Float(related='company_id.scale_factor', readonly=False)

    upload_watermark = fields.Binary(related='company_id.upload_watermark',readonly=False)
    watermark_fname = fields.Char(related='company_id.watermark_fname',readonly=False)


