from odoo import models, fields, api
from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.graphics import renderPM
from reportlab.lib.units import mm, inch, cm, pica
from io import BytesIO
import os, base64, random, re
from odoo.exceptions import ValidationError
from odoo.tools.translate import _
from . import generate_barcode_value as gbv

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    barcode_image = fields.Binary(string="Barcode Image")

    @api.depends('name')
    def _compute_barcode_image_fields_and_button(self):
        # Get the value of the checkbox
        is_generate_barcode = self.env['ir.config_parameter'].sudo().get_param('mh_product_barcode_generator.is_generate_barcode')
        # Set the visibility of fields and button based on the checkbox value
        for record in self:
            record.show_barcode_image_fields_and_button = is_generate_barcode

    # Add a computed boolean field to control the visibility of fields and button
    show_barcode_image_fields_and_button = fields.Boolean(compute='_compute_barcode_image_fields_and_button', store=False, default=False)

    def open_wizard_to_add_barcode(self):
        # Add your logic here
        view_id = self.env.ref('mh_product_barcode_generator.add_update_barcode_wizard_form_view').id
        ctx = self._context.copy()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Add/Update Barcode and Barcode Image'),
            'res_model': 'add.update.barcode.wizard',
            'target': 'new',
            'view_mode': 'form',
            'views': [[view_id, 'form']],
            'context': ctx
        }
        # return {'type': 'ir.actions.act_window_close'}

    # def generate_codabar_value(self):
    #     allowed_chars = r'^[0-9\-$:/.+ABCD]+$'
    #     return ''.join(random.choices(re.findall(allowed_chars, ''), k=10))
    #
    # def generate_code11_value(self):
    #     allowed_chars = r'^[0-9\-]+$'
    #     return ''.join(random.choices(re.findall(allowed_chars, ''), k=10))
    #
    # def generate_code128_value(self):
    #     allowed_chars = r'^[0-9A-Za-z]+$'
    #     return ''.join(random.choices(re.findall(allowed_chars, ''), k=10))
    #
    # def generate_ean5_value(self):
    #     return ''.join(random.choices('0123456789', k=5))
    #
    # def generate_ean8_value(self):
    #     return ''.join(random.choices('0123456789', k=8))
    #
    # def generate_ean13_value(self):
    #     return ''.join(random.choices('0123456789', k=13))
    #
    # def generate_extended_39_value(self):
    #     allowed_chars = r'^[0-9A-Z\-.$/+% ]+$'
    #     return ''.join(random.choices(re.findall(allowed_chars, ''), k=10))
    #
    # def generate_extended_93_value(self):
    #     allowed_chars = r'^[0-9A-Za-z!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\x00]+$'
    #     return ''.join(random.choices(re.findall(allowed_chars, ''), k=10))
    #
    # def generate_fim_value(self):
    #     return 'FIM'
    #
    # def generate_isbn_value(self):
    #     return ''.join(random.choices('0123456789', k=10))
    #
    # def generate_i2of5_value(self):
    #     return ''.join(random.choices('02468', k=10))
    #
    # def generate_msi_value(self):
    #     return ''.join(random.choices('0123456789', k=10))
    #
    # def generate_postnet_value(self):
    #     return ''.join(random.choices('0123456789', k=10))
    #

    #
    # def generate_upca_value(self):
    #     return ''.join(random.choices('0123456789', k=12))
    #
    # def generate_usps_4state_value(self):
    #     return ''.join(random.choices('0123456789', k=10))




    def get_bar_code_value(self,barcode_type):
        try:
            if barcode_type == 'Codabar':
                barcode_value = gbv.generate_codabar_value(self)
            elif barcode_type == 'Code11':
                barcode_value = gbv.generate_code11_value(self)
            elif barcode_type == 'Code128':
                barcode_value = gbv.generate_code128_value(self)
            elif barcode_type == 'EAN5':
                barcode_value = gbv.generate_ean5_value(self)
            elif barcode_type == 'EAN8':
                barcode_value = gbv.generate_ean8_value(self)
            elif barcode_type == 'EAN13':
                barcode_value = gbv.generate_ean13_value(self)
            elif barcode_type == 'Extended39':
                barcode_value = gbv.generate_extended_39_value(self)
            elif barcode_type == 'Extended93':
                barcode_value = gbv.generate_extended_93_value(self)
            elif barcode_type == 'FIM':
                barcode_value = gbv.generate_fim_value(self)
            elif barcode_type == 'ISBN':
                barcode_value = gbv.generate_isbn_value(self)
            elif barcode_type == 'I2of5':
                barcode_value = gbv.generate_i2of5_value(self)
            elif barcode_type == 'MSI':
                barcode_value = gbv.generate_msi_value(self)
            elif barcode_type == 'POSTNET':
                barcode_value = gbv.generate_postnet_value(self)
            elif barcode_type == 'UPCA':
                barcode_value = gbv.generate_upca_value(self)
            elif barcode_type == 'USPS_4State':
                barcode_value = gbv.generate_usps_4state_value(self)

            return barcode_value
        except:
            pass

    @api.depends('barcode')
    def btn_generate_barcode_image(self):
        is_generate_barcode, barcode_type, barcode_width, barcode_height, is_show_barcode_text = self._get_config_settings_values()
        # print('33333333333333',is_generate_barcode, barcode_type, barcode_width, barcode_height, is_show_barcode_text)

        for product in self:
            if product.barcode and not product.barcode_image:  # Check if barcode value exists but no barcode image
                barcode_value = product.barcode
                barcode_image = self._generate_barcode_image(barcode_type, barcode_value, barcode_width,barcode_height, is_show_barcode_text)
                product.barcode_image = barcode_image
            elif not product.barcode:  # Generate both barcode value and image if barcode value doesn't exist
                barcode_value = self.get_bar_code_value(barcode_type)
                barcode_image = self._generate_barcode_image(barcode_type, barcode_value, barcode_width,barcode_height, is_show_barcode_text)
                product.barcode = barcode_value
                product.barcode_image = barcode_image
            elif product.barcode and product.barcode_image:  # Generate both barcode value and image if barcode value doesn't exist
                barcode_value = self.get_bar_code_value(barcode_type)
                barcode_image = self._generate_barcode_image(barcode_type, barcode_value, barcode_width,barcode_height, is_show_barcode_text)
                product.barcode = barcode_value
                product.barcode_image = barcode_image


    def btn_refresh_barcode_image(self):
        if self.barcode:
            is_generate_barcode, barcode_type, barcode_width, barcode_height, is_show_barcode_text = self._get_config_settings_values()
            # barcode_value = self.get_bar_code_value(barcode_type)
            barcode_value = self.barcode
            barcode_image = self._generate_barcode_image(barcode_type, barcode_value, barcode_width, barcode_height,is_show_barcode_text)
            self.barcode_image = barcode_image
        else:
            raise ValidationError('To refresh barcode image, first generate barcode.')


    def _generate_barcode_image(self, barcode_type, barcode, barcode_width, barcode_height, is_show_barcode_text):
        barcode_drawing = createBarcodeDrawing(barcode_type,
            value=barcode,
            format='png',
            barHeight=0.5*inch,
            barWidth = 0.02*inch,
            width = 4 * inch,
            height = 1 * inch,
            humanReadable=is_show_barcode_text)
        buffer = BytesIO()
        renderPM.drawToFile(barcode_drawing, buffer, fmt='png')
        barcode_image = base64.b64encode(buffer.getvalue())
        return barcode_image.decode('utf-8')

    def _get_config_settings_values(self):
        is_generate_barcode = self.env['ir.config_parameter'].sudo().get_param('mh_product_barcode_generator.is_generate_barcode')
        barcode_type = self.env['ir.config_parameter'].sudo().get_param('mh_product_barcode_generator.barcode_type')
        barcode_width = self.env['ir.config_parameter'].sudo().get_param('mh_product_barcode_generator.barcode_width')
        barcode_height = self.env['ir.config_parameter'].sudo().get_param('mh_product_barcode_generator.barcode_height')
        is_show_barcode_text = self.env['ir.config_parameter'].sudo().get_param('mh_product_barcode_generator.is_show_barcode_text')

        # Set default values if not provided
        if is_generate_barcode:
            barcode_type = str(barcode_type) if barcode_type else 'Code128'
            barcode_width = float(barcode_width) if barcode_width else 300.0
            barcode_height = float(barcode_height) if barcode_height else 40.0
            is_show_barcode_text = bool(is_show_barcode_text)
            return bool(is_generate_barcode), barcode_type, barcode_width, barcode_height, is_show_barcode_text
        else:
            raise ValidationError("Check Generate Barcode option from Barcode Settings.")

        # return bool(is_generate_barcode), barcode_type, float(barcode_width), float(barcode_height), bool(is_show_barcode_text)

class ResConfigSettings(models.TransientModel):
    """ Inherit the base settings to add a barcode of product."""
    _inherit = 'res.config.settings'

    is_generate_barcode = fields.Boolean(
        'Geneate Barcode',
        help="If you want to generate barcode than choose this option.",
        config_parameter='mh_product_barcode_generator.is_generate_barcode', default=False)

    barcode_type = fields.Selection([
        ('Codabar', 'Codabar'),
        ('Code11', 'Code-11'),
        ('Extended39', 'Code-39 / Extended-39'),
        ('Extended93', 'Code-93 / Extended-93'),
        ('Code128', 'Code-128'),
        ('EAN5', 'EAN-5'),
        ('EAN8', 'EAN-8'),
        ('EAN13', 'EAN-13'),
        ('FIM', 'FIM'),
        ('ISBN', 'ISBN'),
        ('I2of5', 'Interleaved 2 of 5 Barcode (I2of5)'),
        ('MSI', 'MSI'),
        ('POSTNET', 'POSTNET'),
        ('UPCA', 'UPCA'),
        ('USPS_4State', 'USPS_4State')
    ], "Barcode Type", default='Code128', config_parameter='mh_product_barcode_generator.barcode_type', required=True)

    barcode_size_unit = fields.Selection([
        ('mm', 'mm'),
        ('inch', 'inch'),
        ('cm', 'cm'),
        ('pica', 'pica')
    ], "Barcode Size Unit", default='inch', config_parameter='mh_product_barcode_generator.barcode_size_unit', required=True)

    width = fields.Float(
        'Width',
        help="Adjust the dimensions (width) of the entire barcode drawing",
        config_parameter='mh_product_barcode_generator.barcode_width', default=300)

    height = fields.Float(
        'Height',
        help="Adjust the dimensions (height) of the entire barcode drawing",
        config_parameter='mh_product_barcode_generator.barcode_height', default=40)

    barcode_width = fields.Float(
        'Bar Width',
        help="Adjust the dimensions (bar width) of the bars within the barcode",
        config_parameter='mh_product_barcode_generator.barcode_width', default=300)

    barcode_height = fields.Float(
        'Bar Height',
        help="Adjust the dimensions (bar height) of the bars within the barcode",
        config_parameter='mh_product_barcode_generator.barcode_height', default=40)

    is_show_barcode_text = fields.Boolean(
        'Make this code human readable',
        help="Show barcode text below barcode image",
        config_parameter='mh_product_barcode_generator.is_show_barcode_text', default=False)

    @api.onchange('barcode_type', 'barcode_size_unit')
    def onchange_barcode_type_size_unit(self):
        for rec in self:
            barcode_type = rec.barcode_type
            barcode_size_unit = rec.barcode_size_unit
            if barcode_type and barcode_size_unit:
                barcode_info = {
                    'Codabar': {'mm': (29.2, 12.7, 104.14, 0.25), 'inch': (1.15, 0.5, 4.09, 0.25),
                                'cm': (2.92, 1.27, 10.39, 0.64), 'pica': (6.15, 2.67, 21.83, 1.35)},
                    'Code11': {'mm': (29.2, 12.7, 104.14, 0.25), 'inch': (1.15, 0.5, 4.09, 0.25),
                               'cm': (2.92, 1.27, 10.39, 0.64), 'pica': (6.15, 2.67, 21.83, 1.35)},
                    'Extended39': {'mm': (29.2, 12.7, 104.14, 0.25), 'inch': (1.15, 0.5, 4.09, 0.25),
                                   'cm': (2.92, 1.27, 10.39, 0.64), 'pica': (6.15, 2.67, 21.83, 1.35)},
                    'Extended93': {'mm': (30.5, 22.9, 108.3, 0.79), 'inch': (1.2, 0.9, 4.25, 0.79),
                                   'cm': (3.05, 2.29, 10.8, 2), 'pica': (6.4, 4.8, 22.67, 4.2)},
                    'Code128': {'mm': (30.5, 22.9, 108.3, 0.79), 'inch': (1.2, 0.9, 4.25, 0.79),
                                'cm': (3.05, 2.29, 10.8, 2), 'pica': (6.4, 4.8, 22.67, 4.2)},
                    'EAN5': {'mm': (37.3, 25.9, 130.66, 0.36), 'inch': (1.47, 1.02, 5.21, 0.36),
                             'cm': (3.73, 2.59, 13.24, 0.91), 'pica': (7.85, 5.45, 27.85, 1.92)},
                    'EAN8': {'mm': (23.9, 25.9, 84.35, 0.36), 'inch': (0.94, 1.02, 3.34, 0.36),
                             'cm': (2.39, 2.59, 8.48, 0.91), 'pica': (5.03, 5.45, 17.83, 1.92)},
                    'EAN13': {'mm': (37.3, 25.9, 130.66, 0.36), 'inch': (1.47, 1.02, 5.21, 0.36),
                              'cm': (3.73, 2.59, 13.24, 0.91), 'pica': (7.85, 5.45, 27.85, 1.92)},
                    'FIM': {'mm': (10.2, 8.5, 36.52, 0.43), 'inch': (0.4, 0.33, 1.42, 0.17),
                            'cm': (1.02, 0.85, 3.61, 0.43), 'pica': (2.15, 1.79, 7.59, 0.91)},
                    'ISBN': {'mm': (37.3, 25.9, 130.66, 0.36), 'inch': (1.47, 1.02, 5.21, 0.36),
                             'cm': (3.73, 2.59, 13.24, 0.91), 'pica': (7.85, 5.45, 27.85, 1.92)},
                    'I2of5': {'mm': (105, 29.85, 372.27, 1.05), 'inch': (4.13, 1.17, 14.68, 1.05),
                              'cm': (10.5, 2.99, 37.31, 2.67), 'pica': (22.08, 6.29, 78.48, 5.61)},
                    'MSI': {'mm': (29.2, 12.7, 104.14, 0.25), 'inch': (1.15, 0.5, 4.09, 0.25),
                            'cm': (2.92, 1.27, 10.39, 0.64), 'pica': (6.15, 2.67, 21.83, 1.35)},
                    'POSTNET': {'mm': (114.3, 12.7, 369.48, 0.25), 'inch': (4.5, 0.5, 15.96, 0.25),
                                'cm': (11.43, 1.27, 40.55, 0.64), 'pica': (24, 2.67, 85.33, 1.35)},
                    'UPCA': {'mm': (37.3, 25.9, 130.66, 0.36), 'inch': (1.47, 1.02, 5.21, 0.36),
                             'cm': (3.73, 2.59, 13.24, 0.91), 'pica': (7.85, 5.45, 27.85, 1.92)},
                    'USPS_4State': {'mm': (57.15, 19.05, 203.45, 0.5), 'inch': (2.25, 0.75, 7.99, 0.5),
                                    'cm': (5.715, 1.905, 20.29, 1.27), 'pica': (12, 4, 42.67, 2.67)}
                }
                if barcode_type in barcode_info and barcode_size_unit in barcode_info[barcode_type]:
                    rec.width = barcode_info[barcode_type][barcode_size_unit][2]
                    rec.height = barcode_info[barcode_type][barcode_size_unit][3]
                    rec.barcode_width = barcode_info[barcode_type][barcode_size_unit][0]
                    rec.barcode_height = barcode_info[barcode_type][barcode_size_unit][1]


class AddUpdateBarcodeWizard(models.TransientModel):
    _name = 'add.update.barcode.wizard'

    # Define fields for your wizard here
    update_barcode = fields.Boolean('Update Existing Barcode',help="Also update the existing barcode with the barcode configuration setting.",default=False)

    def add_update_barcode(self):
        products = self.env['product.template'].browse(self.env.context['active_ids'])
        # Products to update
        products_to_update = products
        if not self.update_barcode:
            # If update_barcode checkbox is not checked, filter out products with barcode
            products_to_update = products.filtered(lambda p: not p.barcode)

        for product in products_to_update:
            print('11111111111',product)
            product.btn_generate_barcode_image()
        # return {'type': 'ir.actions.act_window_close'}