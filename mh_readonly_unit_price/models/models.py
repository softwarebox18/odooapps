from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move.line'

    is_readonly = fields.Boolean(
        string="Is Readonly",
        compute='_compute_is_readonly',
        store=False, readonly=False, copy=False, precompute=True)

    @api.depends('company_id')
    def _compute_is_readonly(self):
        has_group = self.env.user.has_group('mh_readonly_unit_price.group_edit_unit_price')
        for order in self:
            if has_group:
                order.is_readonly = has_group
            else:
                order.is_readonly = False


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_readonly = fields.Boolean(
        string="Is Readonly",
        compute='_compute_is_readonly',
        store=False, readonly=False, copy=False, precompute=True)

    @api.depends('company_id')
    def _compute_is_readonly(self):
        has_group = self.env.user.has_group('mh_readonly_unit_price.group_edit_unit_price')
        for order in self:
            if has_group:
                order.is_readonly = has_group
            else:
                order.is_readonly = False


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_readonly = fields.Boolean(
        string="Is Readonly",
        compute='_compute_is_readonly',
        store=False, readonly=False, copy=False, precompute=True)

    @api.depends('company_id','product_template_id')
    def _compute_is_readonly(self):
        has_group = self.env.user.has_group('mh_readonly_unit_price.group_edit_unit_price')
        for order in self:
            if has_group:
                order.is_readonly = has_group
            else:
                order.is_readonly = False
                # if order.product_template_id.type == 'service':
                #     order.is_readonly = True
                # else:
                #     order.is_readonly = False

