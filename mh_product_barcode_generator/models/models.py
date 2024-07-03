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
            if barcode_value is None:
                # Call the function again
                return self.get_bar_code_value(barcode_type)
            else:
                return barcode_value
        except Exception as e:
            print("Error generating barcode value:", e)
            return None

    @api.depends('barcode')
    def btn_generate_barcode_image(self):
        is_generate_barcode, barcode_type, barcode_size_unit, width, height, barcode_width, barcode_height, is_show_barcode_text = self._get_config_settings_values()
        # print('33333333333333',is_generate_barcode, barcode_type, barcode_width, barcode_height, is_show_barcode_text)
        # print('222222222',mm, inch, cm, pica)
        for product in self:
            if product.barcode and not product.barcode_image:  # Check if barcode value exists but no barcode image
                barcode_value = product.barcode
                barcode_image = self._generate_barcode_image(barcode_type, barcode_value, barcode_size_unit, width, height, barcode_width,barcode_height, is_show_barcode_text)
                product.barcode_image = barcode_image
            elif not product.barcode:  # Generate both barcode value and image if barcode value doesn't exist
                barcode_value = self.get_bar_code_value(barcode_type)
                barcode_image = self._generate_barcode_image(barcode_type, barcode_value, barcode_size_unit, width, height, barcode_width,barcode_height, is_show_barcode_text)
                product.barcode = barcode_value
                product.barcode_image = barcode_image
            elif product.barcode and product.barcode_image:  # Generate both barcode value and image if barcode value doesn't exist
                barcode_value = self.get_bar_code_value(barcode_type)
                if barcode_value is None:
                    # Call the function again
                    barcode_value = self.get_bar_code_value(barcode_type)
                else:
                    barcode_value = barcode_value
                barcode_image = self._generate_barcode_image(barcode_type, barcode_value, barcode_size_unit, width, height, barcode_width,barcode_height, is_show_barcode_text)
                product.barcode = barcode_value
                product.barcode_image = barcode_image


    def btn_refresh_barcode_image(self):
        if self.barcode:
            is_generate_barcode, barcode_type, barcode_size_unit, width, height, barcode_width, barcode_height, is_show_barcode_text = self._get_config_settings_values()
            # barcode_value = self.get_bar_code_value(barcode_type)
            barcode_value = self.barcode
            barcode_image = self._generate_barcode_image(barcode_type, barcode_value, barcode_size_unit, width, height, barcode_width, barcode_height,is_show_barcode_text)
            self.barcode_image = barcode_image
        else:
            raise ValidationError('To refresh barcode image, first generate barcode.')


    def _generate_barcode_image(self, barcode_type, barcode, barcode_size_unit, width, height, barcode_width, barcode_height, is_show_barcode_text):
        try:
            if barcode_size_unit == 'mm':
                unit = mm
            elif barcode_size_unit == 'inch':
                unit = inch
            elif barcode_size_unit == 'cm':
                unit = cm
            elif barcode_size_unit == 'pica':
                unit = pica
            # print('-=-=-=-=-=',barcode_type,barcode,width * unit,height * unit,barcode_width * unit,barcode_height * unit,is_show_barcode_text)
            barcode_drawing = createBarcodeDrawing(barcode_type,
                value=barcode,
                format='png',
                width=width * unit,
                height=height * unit,
                barWidth=barcode_width * unit,
                barHeight=barcode_height * unit,
                humanReadable=is_show_barcode_text)

            buffer = BytesIO()
            renderPM.drawToFile(barcode_drawing, buffer, fmt='png')
            barcode_image = base64.b64encode(buffer.getvalue())
            return barcode_image.decode('utf-8')
        except Exception as e:
            # Handle the exception here
            # For now, just print the exception message
            print("Error generating barcode image:", e)
            return None

    def _get_config_settings_values(self):
        is_generate_barcode = self.env['ir.config_parameter'].sudo().get_param('mh_product_barcode_generator.is_generate_barcode')
        barcode_type = self.env['ir.config_parameter'].sudo().get_param('mh_product_barcode_generator.barcode_type')
        barcode_size_unit = self.env['ir.config_parameter'].sudo().get_param('mh_product_barcode_generator.barcode_size_unit')
        width = self.env['ir.config_parameter'].sudo().get_param('mh_product_barcode_generator.width')
        height = self.env['ir.config_parameter'].sudo().get_param('mh_product_barcode_generator.height')
        barcode_width = self.env['ir.config_parameter'].sudo().get_param('mh_product_barcode_generator.barcode_width')
        barcode_height = self.env['ir.config_parameter'].sudo().get_param('mh_product_barcode_generator.barcode_height')
        is_show_barcode_text = self.env['ir.config_parameter'].sudo().get_param('mh_product_barcode_generator.is_show_barcode_text')

        # Set default values if not provided
        if is_generate_barcode:
            barcode_type = str(barcode_type) if barcode_type else 'Code128'
            barcode_size_unit = str(barcode_size_unit) if barcode_size_unit else inch
            width = float(width) if width else 4.25
            height = float(height) if height else 0.79
            barcode_width = float(barcode_width) if barcode_width else 1.20
            barcode_height = float(barcode_height) if barcode_height else 0.90
            is_show_barcode_text = bool(is_show_barcode_text)
            return bool(is_generate_barcode), barcode_type, barcode_size_unit, width, height, barcode_width, barcode_height, is_show_barcode_text
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
        config_parameter='mh_product_barcode_generator.width')

    height = fields.Float(
        'Height',
        help="Adjust the dimensions (height) of the entire barcode drawing",
        config_parameter='mh_product_barcode_generator.height')

    barcode_width = fields.Float(
        'Bar Width',
        help="Adjust the dimensions (bar width) of the bars within the barcode",
        config_parameter='mh_product_barcode_generator.barcode_width')

    barcode_height = fields.Float(
        'Bar Height',
        help="Adjust the dimensions (bar height) of the bars within the barcode",
        config_parameter='mh_product_barcode_generator.barcode_height')

    is_show_barcode_text = fields.Boolean(
        'Make this code human readable',
        help="Show barcode text below barcode image",
        config_parameter='mh_product_barcode_generator.is_show_barcode_text', default=False)

    @api.constrains('width', 'height', 'barcode_width', 'barcode_height')
    def _check_positive_values(self):
        for settings in self:
            if any(field <= 0.0 for field in [settings.width, settings.height, settings.barcode_width, settings.barcode_height]):
                raise ValidationError("Width, height, barcode width, and barcode height must be greater than 0.")


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
            product.btn_generate_barcode_image()
        # return {'type': 'ir.actions.act_window_close'}