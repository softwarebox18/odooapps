# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools, _
from odoo.exceptions import ValidationError

class ResCompanyInh(models.Model):
    _inherit = 'res.company'

    partner_display_fields = fields.Many2many(
        'ir.model.fields',
        'res_company_partner_display_fields_rel',
        'company_id_partner',
        'field_id',
        string="Customer Display Fields",
        domain=lambda self: self._get_partner_domain()
    )

    partner_search_fields = fields.Many2many(
        'ir.model.fields',
        'res_company_partner_search_fields_rel',
        'company_id_partner',
        'field_id',
        string="Customer Search Fields",
        domain=lambda self: self._get_partner_domain()
    )

    def _get_partner_domain(self):
        return [('model', '=', 'res.partner'), ('ttype', 'in', ['char', 'text', 'integer', 'float'])]


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # company_id = fields.Many2one(  # Explicitly add this field
    #     'res.company',
    #     string="Company",
    #     default=lambda self: self.env.company
    # )

    partner_display_fields = fields.Many2many(
        'ir.model.fields',
        related='company_id.partner_display_fields',
        string="Customer Display Fields",
        readonly=False
    )

    partner_search_fields = fields.Many2many(
        'ir.model.fields',
        related='company_id.partner_search_fields',
        string="Customer Search Fields",
        readonly=False
    )

    # def set_values(self):
    #     super(ResConfigSettings, self).set_values()


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if not args:
            args = []

        # Default search field
        search_fields = ['name']

        # Fetch additional fields from company settings
        company = self.env.company
        if company.partner_search_fields:
            search_fields.extend(company.partner_search_fields.mapped('name'))

        # Construct the dynamic search domain with OR conditions
        domain = ['|'] * (len(search_fields) - 1)
        for field in search_fields:
            domain.append((field, operator, name))

        return self.search(domain + args, limit=limit).name_get()

    def name_get(self):
        result = []
        company = self.env.company
        display_fields = company.partner_display_fields.mapped('name') if company.partner_display_fields else []

        for partner in self:
            values = [partner.name]  # Always include default name field

            for field in display_fields:
                value = getattr(partner, field, None)
                if value:
                    values.append(str(value))  # Convert to string

            display_name = " | ".join(values)  # Format display name
            result.append((partner.id, display_name))

        return result

