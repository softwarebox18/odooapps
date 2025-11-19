from odoo import models, fields, _
from odoo.exceptions import ValidationError
import json

class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('moamalat_lightbox', "Moamalat LightBox")],
        ondelete={'moamalat_lightbox': 'set default'},
    )
    moamalat_mid = fields.Char(string="Merchant ID", required_if_provider='moamalat_lightbox')
    moamalat_tid = fields.Char(string="Terminal ID", required_if_provider='moamalat_lightbox')
    moamalat_secret = fields.Char(string="Secret (Hex)", required_if_provider='moamalat_lightbox')

    def _moamalat_get_inline_form_values(self, currency=None):
        self.ensure_one()
        return json.dumps({
            'provider_id': self.id,
            'mid': self.moamalat_mid,
            'tid': self.moamalat_tid,
            'currency': currency.name if currency else None,
        })

    def _get_supported_currencies(self):
        currencies = super()._get_supported_currencies()
        if self.code == 'moamalat_lightbox':
            # adjust if Moamalat supports specific currencies only
            return currencies.filtered(lambda c: c.name in ['LYD','USD'])  # example
        return currencies
