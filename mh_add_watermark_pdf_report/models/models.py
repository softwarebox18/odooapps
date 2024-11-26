# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
import io,os
from base64 import urlsafe_b64decode
from logging import getLogger

from PIL import Image, ImageDraw, ImageFont, ImageColor
from PyPDF2 import PdfFileReader, PdfFileWriter

from odoo.exceptions import UserError

try:
    from PyPDF2.errors import PdfReadError
except ImportError:
    from PyPDF2.utils import PdfReadError


LOGGER = getLogger(__name__)

class inherit_ir_actions_report(models.Model):

    _inherit = 'ir.actions.report'

    watermark_type = fields.Selection(
        [('Text Watermark', 'Text Watermark'), ('Image or PDF Watermark', 'Image or PDF Watermark')],
        string="Watermark Type", company_dependent=True)
    watermark_text = fields.Char('Watermark Text', company_dependent=True)
    font_name = fields.Selection([('Arial', 'Arial'), ('Arial Bold', 'Arial Bold'), ('Arial Italic', 'Arial Italic'),
                                  ('Times New Roman', 'Times New Roman'),
                                  ('Times New Roman Bold', 'Times New Roman Bold'),
                                  ('Times New Roman Italic', 'Times New Roman Italic')], string="Font Name",
                                 company_dependent=True)
    font_size = fields.Integer('Font Size', company_dependent=True, default=100, phaceholder="100")
    font_color = fields.Selection(
        [('Red', 'Red'), ('Green', 'Green'), ('Blue', 'Blue'), ('Yellow', 'Yellow'), ('Gray', 'Gray'),
         ('Black', 'Black')], string="Font Color", company_dependent=True)
    opacity = fields.Integer('Opacity', company_dependent=True, default=128, phaceholder="0 to 255")
    rotation = fields.Integer('Rotation Angle', company_dependent=True, default=45, phaceholder="45")
    scale_factor = fields.Float('Sacle Factor', company_dependent=True, default=1, placeholder="1")

    upload_watermark = fields.Binary('Upload Watermark (PDF/Image)',company_dependent=True, help="""Upload a PDF or Image file to be used as the watermark, appearing as the background on each printed page. The watermark uploaded here will take precedence over the one set in the company's general settings.""")
    watermark_fname = fields.Char('Watermark Filename', company_dependent=True)



class ir_actions_report(models.Model):
    _inherit = "ir.actions.report"

    def _render_qweb_pdf(self, report_ref, res_ids=None, data=None):
        result = super(ir_actions_report, self)._render_qweb_pdf(report_ref, res_ids, data)
        ir_actions_obj = self._get_report(report_ref)
        if result:
            watermark_type = ir_actions_obj.watermark_type if ir_actions_obj.watermark_type else (self.env.company.watermark_type if self.env.company.watermark_type else None)
            # watermark_type = (ir_actions_obj.watermark_type or self.env.company.watermark_type or None)
            if watermark_type == 'Text Watermark':
                watermark_text = ir_actions_obj.watermark_text if ir_actions_obj.watermark_type else (self.env.company.watermark_text if self.env.company.watermark_type else None)
                # watermark_text = (ir_actions_obj.watermark_text or self.env.company.watermark_text or None)
                # Current file's directory (e.g., /path/to/module/models/)
                current_file_dir = os.path.dirname(os.path.realpath(__file__))
                # Go up one directory to get to the module's root
                module_dir = os.path.abspath(os.path.join(current_file_dir, '..'))
                # Construct the font file path
                font_name = ir_actions_obj.font_name if ir_actions_obj.watermark_type else (self.env.company.font_name if self.env.company.watermark_type else None)
                # font_name = (ir_actions_obj.font_name or self.env.company.font_name)
                font_file_path = os.path.join(module_dir, 'static', 'src', 'fonts', font_name + '.ttf')
                # print(font_file_path)  # Verify the pat
                # print(os.path.exists(font_file_path))  # Should print True if the file existsh
                font_size = ir_actions_obj.font_size if ir_actions_obj.watermark_type else (self.env.company.font_size if self.env.company.watermark_type else 100)
                # font_size = (ir_actions_obj.font_size or self.env.company.font_size or 100)
                font_color = ir_actions_obj.font_color if ir_actions_obj.watermark_type else (self.env.company.font_color if self.env.company.watermark_type else "red")
                # font_color = (ir_actions_obj.font_color or self.env.company.font_color or "red")
                rotation = ir_actions_obj.rotation if ir_actions_obj.watermark_type else (self.env.company.rotation if self.env.company.watermark_type else 45)
                # rotation = (ir_actions_obj.rotation or self.env.company.rotation or 45)
                opacity = ir_actions_obj.opacity if ir_actions_obj.watermark_type else (self.env.company.opacity if self.env.company.watermark_type else 100)
                # opacity = (ir_actions_obj.opacity or self.env.company.opacity or 100)
                # Convert color name to RGBA
                text_color = ImageColor.getrgb(font_color.lower()) + (opacity,)  # Add opacity to RGB tuple

                # Handle watermark as text
                if watermark_text:
                    try:
                        # Create an image with text
                        font = ImageFont.truetype(font_file_path, font_size)  # Adjust the font path as needed
                        text_width, text_height = font.getsize(watermark_text)
                        image_size = (text_width + 40, text_height + 40)  # Add padding around the text

                        # Create a blank transparent image
                        image = Image.new("RGBA", image_size, (255, 255, 255, 0))  # Fully transparent background
                        draw = ImageDraw.Draw(image)

                        # Add text to the image with transparency
                        # text_color = (0, 0, 0, 128)  # Black text with 50% opacity (alpha=128)
                        draw.text((20, 20), watermark_text, fill=text_color, font=font)  # Adjust padding as needed

                        # Rotate the image
                        image = image.rotate(rotation, expand=1)

                        # Convert RGBA to RGB while preserving transparency as white
                        rgb_image = Image.new("RGB", image.size, (255, 255, 255))  # White background
                        rgb_image.paste(image, mask=image.split()[3])  # Use alpha channel as mask to merge transparency

                        # Convert the image to a PDF
                        pdf_buffer = io.BytesIO()
                        resolution = ir_actions_obj.paperformat_id.dpi or 90
                        rgb_image.save(pdf_buffer, "PDF", resolution=resolution)

                        # Load the PDF for merging
                        pdf_image_watermark = PdfFileReader(pdf_buffer)
                    except Exception:
                        LOGGER.exception("Failed to create the text watermark...")

            elif watermark_type == 'Image or PDF Watermark':
                # Get watermark
                watermark = ir_actions_obj.upload_watermark if ir_actions_obj.watermark_type else (self.env.company.upload_watermark if self.env.company.watermark_type else None)
                # watermark = (ir_actions_obj.upload_watermark or self.env.company.upload_watermark or None)
                if not watermark:
                    return result

                if watermark:
                    # Handle watermark as PDF or image
                    watermark = urlsafe_b64decode(watermark)


                    pdf_image_watermark = None
                    try:
                        pdf_image_watermark = PdfFileReader(io.BytesIO(watermark))
                        if pdf_image_watermark.isEncrypted:
                            pdf_image_watermark.decrypt("")
                    except Exception:
                        try:
                            image = Image.open(io.BytesIO(watermark))
                            pdf_buffer = io.BytesIO()
                            if image.mode != "RGB":
                                image = image.convert("RGB")
                            resolution = image.info.get("dpi", ir_actions_obj.paperformat_id.dpi or 90)
                            if isinstance(resolution, tuple):
                                resolution = resolution[0]
                            # Save the image as PDF
                            image.save(pdf_buffer, "pdf", resolution=resolution)
                            pdf_image_watermark = PdfFileReader(pdf_buffer)
                        except Exception:
                            LOGGER.exception("Failed to load the watermark...")

                    # Check if watermark is valid
                    if not pdf_image_watermark or pdf_image_watermark.numPages < 1:
                        LOGGER.info("Invalid watermark PDF or image")
                        return result
            else:
                return result

            pdf = PdfFileWriter()
            doc = PdfFileReader(io.BytesIO(result[0]))

            # Iterate through each page in the report
            for page in doc.pages:
                page_width = page.mediaBox.getWidth()
                page_height = page.mediaBox.getHeight()

                # Dynamically scale watermark to a percentage of the page dimensions
                watermark_page = pdf.addBlankPage(page_width, page_height)
                pdf_page = pdf_image_watermark.getPage(0)

                watermark_width = pdf_page.mediaBox.getWidth()
                watermark_height = pdf_page.mediaBox.getHeight()

                # Calculate scaling factors
                scale_factor = ir_actions_obj.scale_factor if ir_actions_obj.watermark_type else (self.env.company.scale_factor if self.env.company.watermark_type else 1)
                # scale_factor = (ir_actions_obj.scale_factor or self.env.company.scale_factor or 1)
                # scale_factor = 0.5  # 0.5 Scale watermark to 50% of page width
                scaled_width = page_width * scale_factor
                scaled_height = float(watermark_height) * (float(scaled_width) / float(watermark_width))

                # Ensure watermark height doesn't exceed page height
                if scaled_height > page_height * scale_factor:
                    scaled_height = page_height * scale_factor
                    scaled_width = float(watermark_width) * (float(scaled_height) / float(watermark_height))

                # Center offsets for the scaled watermark
                x_offset = (page_width - scaled_width) / 2
                y_offset = (page_height - scaled_height) / 2

                # Apply scaling and position
                watermark_page.mergeScaledTranslatedPage(pdf_page, scaled_width / float(watermark_width), x_offset,y_offset)

                # Overlay the original page content
                watermark_page.mergePage(page)

            # Iterate through each page in the report
            # for page in doc.pages:
            #     page_width = page.mediaBox.getWidth()
            #     page_height = page.mediaBox.getHeight()
            #
            #     watermark_page = pdf.addBlankPage(page_width, page_height)
            #     pdf_page = pdf_image_watermark.getPage(0)
            #
            #     watermark_width = pdf_page.mediaBox.getWidth()
            #     watermark_height = pdf_page.mediaBox.getHeight()
            #
            #     # Calculate center offsets for the watermark
            #     x_offset = (page_width - watermark_width) / 2
            #     y_offset = (page_height - watermark_height) / 2
            #
            #     # Merge watermark into the blank page
            #     watermark_page.mergeTranslatedPage(pdf_page, x_offset, y_offset)
            #
            #     # Overlay the original page content
            #     watermark_page.mergePage(page)

            # Write the final PDF
            result = io.BytesIO()
            pdf.write(result)
            return result.getvalue(), "pdf"

        return result

