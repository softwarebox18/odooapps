from odoo import models, fields, api

class ResCompanyInh(models.Model):
    _inherit = 'res.company'

    show_sr_no_in_report = fields.Boolean(
        string='Display Serial Number in Report',
        default=False,
        help="Display Serial Number in Quotation / Sale Order Report",
    )

    show_product_img_in_report = fields.Boolean(
        string='Display Product Image in Report',
        default=False,
        help="Display Product Image in Quotation / Sale Order Report",
    )

class SaleConfigSett(models.TransientModel):
    _inherit = 'res.config.settings'

    show_sr_no_in_report = fields.Boolean(
        related='company_id.show_sr_no_in_report',
        string="Show Serial Number in Report",
        readonly=False,
        help="Display Serial Number in Quotation / Sale Order Report"
    )

    show_product_img_in_report = fields.Boolean(
        related='company_id.show_product_img_in_report',
        string="Display Product Image in Report",
        readonly=False,
        help="Display Product Image in Quotation / Sale Order Report"
    )

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    serial_number = fields.Char(string="S.N.", help="Serial number or custom string for this line",
                                compute="_compute_serial_number", store=True, readonly=False, copy=False, precompute=True)

    @api.depends('order_id', 'order_id.order_line')
    def _compute_serial_number(self):
        """
        Automatically assign or reset serial numbers based on changes in order lines:
        - If a serial number is manually set to a non-digit (e.g., "F_1"), the numbering for subsequent lines restarts from 1.
        - Automatically assigns sequential numbers for newly added lines.
        """
        for line in self:
            if not line.order_id:
                continue

            lines = line.order_id.order_line
            reset_index = None  # Tracks the index where numbering needs to restart

            for idx, current_line in enumerate(lines):
                # Check if the serial number was manually set to a non-digit value
                if current_line.serial_number and not current_line.serial_number.isdigit():
                    reset_index = idx + 1  # Start resetting from the next line
                    continue

                # Auto-assign numbers based on reset index or sequentially
                if reset_index is not None and idx >= reset_index:
                    current_line.serial_number = str(idx - reset_index + 1)
                elif not current_line.serial_number or current_line.serial_number.isdigit():
                    current_line.serial_number = str(idx + 1)

    image_line = fields.Image("Product Image",help="Upload an image for this line. It won't affect the product's saved image.")
    display_image = fields.Image("Display Image", compute="_compute_display_image", store=True)

    @api.depends('product_template_id','image_line', 'product_template_id.image_1920')
    def _compute_display_image(self):
        for line in self:
            if line.image_line:
                line.display_image = line.image_line
            else:
                line.display_image = line.product_template_id.image_1920
                line.image_line = line.product_template_id.image_1920

    @api.onchange('product_template_id')
    def _onchange_product_template_id(self):
        """ Update display image immediately when product is selected. """
        for line in self:
            if not line.image_line and line.product_template_id.image_1920:
                line.display_image = line.product_template_id.image_1920
                line.image_line = line.product_template_id.image_1920

