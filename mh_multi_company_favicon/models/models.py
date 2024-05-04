# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools, _
from odoo.modules.module import get_resource_path
from random import randrange
from PIL import Image
import base64
import io
import logging
import os

class ResCompany(models.Model):
    _inherit = 'res.company'

    favicon = fields.Binary(
        string="Company Favicon",
        help="This field holds the image used to display a favicon for a given company."
    )

    @api.depends('favicon')
    def _compute_favicon_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for company in self:
            if company.favicon:
                company.favicon_url = f"data:image/x-icon;base64,{company.favicon.decode('utf-8')}"
            else:
                company.favicon_url = f"{base_url}/web/static/img/favicon.ico"

    favicon_url = fields.Char(
        string="Favicon URL",
        compute='_compute_favicon_url',
        store=True,
        help="URL of the favicon for this company."
    )



    # def _get_default_favicon(self, original=False):
    #     img_path = get_resource_path('web', 'static/img/favicon.ico')
    #     with tools.file_open(img_path, 'rb') as f:
    #         if original:
    #             return base64.b64encode(f.read())
    #         # Modify the source image to add a colored bar on the bottom
    #         # This could seem overkill to modify the pixels 1 by 1, but
    #         # Pillow doesn't provide an easy way to do it, and this
    #         # is acceptable for a 16x16 image.
    #         color = (randrange(32, 224, 24), randrange(32, 224, 24), randrange(32, 224, 24))
    #         original = Image.open(f)
    #         new_image = Image.new('RGBA', original.size)
    #         height = original.size[1]
    #         width = original.size[0]
    #         bar_size = 1
    #         for y in range(height):
    #             for x in range(width):
    #                 pixel = original.getpixel((x, y))
    #                 if height - bar_size <= y + 1 <= height:
    #                     new_image.putpixel((x, y), (color[0], color[1], color[2], 255))
    #                 else:
    #                     new_image.putpixel((x, y), (pixel[0], pixel[1], pixel[2], pixel[3]))
    #         stream = io.BytesIO()
    #         new_image.save(stream, format="ICO")
    #         return base64.b64encode(stream.getvalue())
    #
    # favicon = fields.Binary(string="Company Favicon",help="This field holds the image used to display a favicon for a given company.", default=_get_default_favicon)
