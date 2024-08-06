from odoo import models, fields

class SaleReportExtended(models.Model):
    _inherit = 'sale.report'

    standard_price = fields.Float(string='Cost Price', readonly=True)

    # def _select_sale(self):
    #     select_ = super(SaleReportExtended, self)._select_sale()
    #     select_ += ", ip.value_float AS standard_price"
    #     return select_

    def _select_additional_fields(self):
        _select_additional = super()._select_additional_fields()
        _select_additional['standard_price'] = "ip.value_float"
        return _select_additional

    def _group_by_sale(self):
        group_by_ = super(SaleReportExtended, self)._group_by_sale()
        group_by_ += ", ip.value_float"
        return group_by_

    def _from_sale(self):
        from_ = super(SaleReportExtended, self)._from_sale()
        from_ += """
            LEFT JOIN ir_property ip ON ip.res_id = CONCAT('product.product,', l.product_id) AND ip.name = 'standard_price'
        """
        return from_
