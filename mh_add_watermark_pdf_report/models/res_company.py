# -*- coding: utf-8 -*-
from odoo import api, fields, models

class res_company(models.Model):

    _inherit = ["res.company"]

    watermark_type = fields.Selection([('Text Watermark', 'Text Watermark'),('Image or PDF Watermark', 'Image or PDF Watermark')], string="Watermark Type", company_dependent=True)
    watermark_text = fields.Char('Watermark Text', company_dependent=True)
    font_name = fields.Selection([('Arial', 'Arial'),('Arial Bold', 'Arial Bold'),('Arial Italic', 'Arial Italic'),('Times New Roman', 'Times New Roman'),('Times New Roman Bold', 'Times New Roman Bold'),('Times New Roman Italic', 'Times New Roman Italic')], string="Font Name", company_dependent=True)
    font_size = fields.Integer('Font Size', company_dependent=True, default=100, placeholder="100")
    font_color = fields.Selection([('Red', 'Red'),('Green', 'Green'),('Blue', 'Blue'),('Yellow', 'Yellow'),('Gray', 'Gray'),('Black', 'Black')], string="Font Color", company_dependent=True)
    opacity = fields.Integer('Opacity', company_dependent=True, default=128, placeholder="0 to 255")
    rotation = fields.Integer('Rotation', company_dependent=True, default=45, placeholder="45")
    scale_factor = fields.Float('Sacle Factor', company_dependent=True, default=1, placeholder="1")

    upload_watermark = fields.Binary('Upload Watermark (PDF/Image)', company_dependent=True,help="""Upload a PDF or Image file to be used as the watermark, appearing as the background on each printed page. The watermark uploaded here will take precedence over the one set in the company's general settings.""")
    watermark_fname = fields.Char('Watermark Filename', company_dependent=True)




