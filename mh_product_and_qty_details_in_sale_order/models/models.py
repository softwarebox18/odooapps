# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools, _

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    order_line_info = fields.Html(string="Order Details", compute='_compute_order_line_info')

    @api.depends('order_line.product_id', 'order_line.product_uom_qty')
    def _compute_order_line_info(self):
        for order in self:
            lines_info = []
            for line in order.order_line:
                product_name = line.product_id.name
                quantity = line.product_uom_qty
                lines_info.append(f"<b>{product_name}</b>: {quantity}")
            order.order_line_info = "<br/>".join(lines_info)