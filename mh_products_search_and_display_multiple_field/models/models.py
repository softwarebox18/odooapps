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

        # Default search field
        search_fields = ['name']

        # Fetch additional fields from company settings
        company = self.env.company
        if company.product_search_fields:
            search_fields.extend(company.product_search_fields.mapped('name'))

        # Construct the dynamic search domain with OR conditions
        domain = ['|'] * (len(search_fields) - 1)
        for field in search_fields:
            domain.append((field, operator, name))

        products = self.search(domain + args, limit=limit)

        # Fetch fields for display
        display_fields = company.product_display_fields.mapped('name') if company.product_display_fields else []

        # Manually construct the display names
        result = []
        for product in products:
            values = [product.name]  # Always include default name field

            for field in display_fields:
                value = getattr(product, field, None)
                if value:  # Avoid empty values
                    # If it's a many2one field, use its display_name
                    if isinstance(value, models.BaseModel):
                        values.append(value.display_name)
                    else:
                        values.append(str(value))

            display_name = " | ".join(values)  # Format display name
            result.append((product.id, display_name))

        return result

    @api.depends("name")  # Forces Odoo to refresh the Many2One field
    def _compute_display_name(self):
        for rec in self:
            search_result = rec.name_search(rec.name)  # Get search results
            rec.display_name = search_result[0][1] if search_result else rec.name  # Default to `name` if no match


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if not args:
            args = []

        # Default search field
        search_fields = ['name']

        # Fetch additional fields from company settings
        company = self.env.company
        if company.product_search_fields:
            search_fields.extend(company.product_search_fields.mapped('name'))

        # Construct the dynamic search domain with OR conditions
        domain = ['|'] * (len(search_fields) - 1)
        for field in search_fields:
            domain.append((field, operator, name))

        products = self.search(domain + args, limit=limit)

        # Fetch fields for display
        display_fields = company.product_display_fields.mapped('name') if company.product_display_fields else []

        # Manually construct the display names
        result = []
        for product in products:
            values = [product.name]  # Always include default name field

            for field in display_fields:
                value = getattr(product, field, None)
                if value:  # Avoid empty values
                    # If it's a many2one field, use its display_name
                    if isinstance(value, models.BaseModel):
                        values.append(value.display_name)
                    else:
                        values.append(str(value))

            display_name = " | ".join(values)  # Format display name
            result.append((product.id, display_name))

        return result

    @api.depends("name")  # Forces Odoo to refresh the Many2One field
    def _compute_display_name(self):
        for rec in self:
            search_result = rec.name_search(rec.name)  # Get search results
            rec.display_name = search_result[0][1] if search_result else rec.name  # Default to `name` if no match

