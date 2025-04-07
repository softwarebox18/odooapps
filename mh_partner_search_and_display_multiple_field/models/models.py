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
        return [('model', '=', 'res.partner'), ('ttype', 'in', ['char', 'text', 'integer', 'float', 'selection', 'many2one'])]


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

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
                if value not in [None, False]:  # Avoid empty values
                    # If it's a many2one field, use its display_name
                    if isinstance(value, models.BaseModel):
                        values.append(value.display_name)
                    else:
                        values.append(str(value))

            display_name = " | ".join(filter(None, values))  # Remove empty values

            result.append((partner.id, display_name))

        return result

    @api.depends("name")  # Forces Odoo to refresh the Many2One field
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = rec.name_get()[0][1] if rec else ""

