from odoo import fields, models, tools

class PosOrderReport(models.Model):
    _inherit = "report.pos.order"

    payment_method_id = fields.Many2one('pos.payment.method', string='Payment Method', readonly=True)
    payment_amount = fields.Float(string='Payment Amount', readonly=True)

    def _select(self):
        return super(PosOrderReport, self)._select() + """
            , pm.id AS payment_method_id
            , SUM(pp.amount) AS payment_amount
        """

    def _from(self):
        return super(PosOrderReport, self)._from() + """
            LEFT JOIN pos_payment pp ON (s.id = pp.pos_order_id)
            LEFT JOIN pos_payment_method pm ON (pp.payment_method_id = pm.id)
        """

    def _group_by(self):
        return super(PosOrderReport, self)._group_by() + ", pm.id"

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                %s
                %s
                %s
            )
        """ % (self._table, self._select(), self._from(), self._group_by()))
