# controllers/main.py
from odoo import http
from odoo.http import request
import hmac
import hashlib
import binascii
from binascii import unhexlify

class MoamalatController(http.Controller):
    """
    Endpoints:
     - /payment/moamalat/get_secure_hash  (POST json) -> returns secure_hash
     - /payment/moamalat/return           (POST json) -> receives LightBox result and updates tx
    """

    @http.route('/payment/moamalat/get_secure_hash', type='json', auth='public', methods=['POST'])
    def get_secure_hash(self, provider_id, amount, merchantReference, trxDateTime, **kwargs):
        """
        Generate Moamalat SecureHash using SHA-256 HMAC
        Fields: Amount, DateTimeLocalTrxn, MerchantId, MerchantReference, TerminalId
        """

        # Get your merchant configuration from the provider_id
        provider = request.env['payment.provider'].sudo().browse(provider_id)
        merchant_id = provider.moamalat_mid  # Moamalat MerchantId
        terminal_id = provider.moamalat_tid  # Moamalat TerminalId
        secret_key_hex = provider.moamalat_secret  # Moamalat Secret Key (hex)

        # Ensure secret key is in bytes
        secret_key = binascii.unhexlify(secret_key_hex)

        # Build the string in exact order
        string_to_hash = (
            f"Amount={amount}&"
            f"DateTimeLocalTrxn={trxDateTime}&"
            f"MerchantId={merchant_id}&"
            f"MerchantReference={merchantReference}&"
            f"TerminalId={terminal_id}"
        )

        # Compute HMAC SHA-256
        secure_hash = hmac.new(secret_key, string_to_hash.encode('utf-8'), hashlib.sha256).hexdigest().upper()

        # Return values to frontend
        return {
            'mid': merchant_id,
            'tid': terminal_id,
            'AmountTrxn': amount,
            'MerchantReference': merchantReference,
            'DateTimeLocalTrxn': trxDateTime,
            'secure_hash': secure_hash,
        }

    @http.route('/payment/moamalat/return', type='json', auth='public', methods=['POST'])
    def moamalat_return(self, **post):

        reference = post.get('MerchantReference') or post.get('reference')
        access_token = post.get('access_token')

        tx_obj = request.env['payment.transaction'].sudo()

        tx = None

        # 1) Find draft transaction created during checkout
        if reference:
            domain = [
                ('reference', '=', reference),
                ('provider_code', '=', 'moamalat_lightbox'),
            ]
            if access_token:
                domain.append(('access_token', '=', access_token))

            tx = tx_obj.search(domain, limit=1)

        # 2) Fallback to standard method
        if not tx:
            tx = tx_obj._get_tx_from_notification_data('moamalat_lightbox', post)

        if not tx:
            return {'result': 'error', 'message': 'Transaction not found'}

        # Call Odoo handling → YOUR METHOD is triggered automatically
        tx._process_notification_data(post)

        return {'result': 'success'}

    # @http.route('/payment/moamalat/return', type='json', auth='public', methods=['POST'])
    # def moamalat_return(self, **post):
    #     """
    #     Called after Lightbox completes. 'post' contains returned fields + access_token.
    #     """
    #     tx = request.env['payment.transaction'].sudo()._get_tx_from_notification_data(
    #         'moamalat_lightbox', post
    #     )
    #     if not tx:
    #         return {'result': 'error', 'message': 'Transaction not found'}
    #     tx._handle_notification_data('moamalat_lightbox', post)
    #     return {'result': 'success'}







