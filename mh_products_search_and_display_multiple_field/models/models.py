from odoo import models, fields, api

class ResCompanyInh(models.Model):
    _inherit = 'res.company'

    product_display_fields = fields.Many2many(
        'ir.model.fields',
        'res_company_product_display_fields_rel',
        'company_id_product',
        'field_id',
        string="Product Display Fields",
        domain=lambda self: self._get_product_domain()
    )

    product_search_fields = fields.Many2many(
        'ir.model.fields',
        'res_company_product_search_fields_rel',
        'company_id_product',
        'field_id',
        string="Product Search Fields",
        domain=lambda self: self._get_product_domain()
    )

    def _get_product_domain(self):
        return [('model', '=', 'product.product'), ('ttype', 'in', ['char', 'text', 'integer', 'float', 'selection', 'many2one'])]


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    product_display_fields = fields.Many2many(
        'ir.model.fields',
        related='company_id.product_display_fields',
        string="Product Display Fields",
        readonly=False
    )

    product_search_fields = fields.Many2many(
        'ir.model.fields',
        related='company_id.product_search_fields',
        string="Product Search Fields",
        readonly=False
    )


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if not args:
            args = []

        # Default search fields
        search_fields = ['name']

        # Fetch additional fields from company settings
        company = self.env.company
        if company.product_search_fields:
            search_fields.extend(company.product_search_fields.mapped('name'))

        # Construct the dynamic search domain with OR conditions
        domain = ['|'] * (len(search_fields) - 1)
        for field in search_fields:
            domain.append((field, operator, name))

        return self.search(domain + args, limit=limit).name_get()

    def name_get(self):
        result = []
        company = self.env.company
        display_fields = company.product_display_fields.mapped('name') if company.product_display_fields else []

        for product in self:
            values = [product.name]  # Always include default name field

            for field in display_fields:
                value = getattr(product, field, None)
                if value not in [None, False]:  # Avoid empty values
                    # If it's a many2one field, use its display_name
                    if isinstance(value, models.BaseModel):
                        values.append(value.display_name)
                    else:
                        values.append(str(value))
                    # values.append(str(value))  # Convert to string

            display_name = " | ".join(filter(None, values))  # Remove empty values

            result.append((product.id, display_name))

        return result

    @api.depends("name")  # Forces Odoo to refresh the Many2One field
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = rec.name_get()[0][1] if rec else ""