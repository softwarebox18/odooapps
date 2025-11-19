# models/payment_transaction.py
from odoo import models, fields, _
from odoo.exceptions import ValidationError

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    # fields to store provider-specific info

    moamalat_system_reference = fields.Char("Moamalat System Reference", readonly=True)
    moamalat_network_reference = fields.Char("Moamalat Network Reference", readonly=True)
    moamalat_payer_account = fields.Char("Payer Card Number", readonly=True)
    moamalat_payer_name = fields.Char("Payer Name", readonly=True)
    moamalat_txn_date = fields.Char("Transaction Date", readonly=True)

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        txs = super()._get_tx_from_notification_data(provider_code, notification_data)

        # Always handle moamalat manually
        if provider_code != 'moamalat_lightbox':
            return txs

        # Try ALL possible reference key names
        reference = (
                notification_data.get('MerchantReference')
                or notification_data.get('merchantReference')
                or notification_data.get('reference')
                or notification_data.get('Reference')
        )

        if not reference:
            raise ValidationError(_("Moamalat: No reference in notification data: %s") % notification_data)

        # Search by our own reference format
        tx = self.search([
            ('reference', '=', reference),
            ('provider_code', '=', 'moamalat_lightbox')
        ], limit=1)

        if not tx:
            raise ValidationError(
                _("Moamalat: No transaction found for reference %s.") % reference
            )

        return tx


    def _process_notification_data(self, notification_data):
        super()._process_notification_data(notification_data)

        if self.provider_code != 'moamalat_lightbox':
            return

        # Extract values
        system_ref = notification_data.get('SystemReference')
        network_ref = notification_data.get('NetworkReference')
        payer_account = notification_data.get('PayerAccount')
        payer_name = notification_data.get('PayerName')
        txn_date = notification_data.get('TxnDate')

        # Store in transaction fields
        self.moamalat_system_reference = system_ref
        self.moamalat_network_reference = network_ref
        self.moamalat_payer_account = payer_account
        self.moamalat_payer_name = payer_name
        self.moamalat_txn_date = txn_date

        # REQUIRED by Odoo: provider_reference (unique ID from gateway)
        if system_ref:
            self.provider_reference = system_ref

        # Determine success (Moamalat has no ResponseCode)
        if system_ref and network_ref:
            self._set_done()
        else:
            message = _("Moamalat: payment failed or incomplete (missing SystemReference / NetworkReference).")
            self._set_canceled(state_message=message)


