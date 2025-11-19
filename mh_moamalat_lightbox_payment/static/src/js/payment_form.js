/** @odoo-module **/

import paymentForm from '@payment/js/payment_form';
import { rpc } from '@web/core/network/rpc';

paymentForm.include({

    async _prepareInlineForm(providerId, providerCode, paymentOptionId, paymentMethodCode, flow) {
        if (providerCode !== 'moamalat_lightbox') {
            return this._super(...arguments);
        }

        // Only prepare UI – NOT transaction creation
        const radio = document.querySelector('input[name="o_payment_radio"]:checked');
        if (!radio) {
            return this._super(...arguments);
        }

        this.inlineValues = JSON.parse(radio.dataset.moamalatInlineFormValues || "{}");
    },

    // ╔══════════════════════════════════════════════════════╗
    // ║     THIS is where Odoo creates payment.transaction    ║
    // ╚══════════════════════════════════════════════════════╝
    async _initiatePaymentFlow(providerCode, paymentOptionId, paymentMethodCode, flow) {
        if (providerCode !== 'moamalat_lightbox') {
            return this._super(...arguments);
        }

        // 1️⃣ Create Odoo payment.transaction
        let txValues;
        try {
            txValues = await rpc(
                this.paymentContext.transactionRoute,
                this._prepareTransactionRouteParams()
            );
        } catch (e) {
            this._displayErrorDialog("Transaction Error", e.message);
            this._enableButton();
            return;
        }

        const reference = txValues.reference;
        const access_token = txValues.access_token;

        // 2️⃣ Prepare Moamalat Lightbox request
        const amount = Math.round((this.paymentContext.amount || 0) * 100);

        const now = new Date();
        const trxDateTime =
            String(now.getFullYear()).slice(2) +
            String(now.getMonth() + 1).padStart(2, "0") +
            String(now.getDate()).padStart(2, "0") +
            String(now.getHours()).padStart(2, "0") +
            String(now.getMinutes()).padStart(2, "0") +
            String(now.getSeconds()).padStart(2, "0");

        // 3️⃣ Request secure hash
        let secureData;
        try {
            secureData = await rpc('/payment/moamalat/get_secure_hash', {
                provider_id: txValues.provider_id,
                amount: amount,
                merchantReference: reference,
                trxDateTime: trxDateTime,
            });
        } catch (e) {
            this._displayErrorDialog("Hash Error", e.message);
            this._enableButton();
            return;
        }

        // 4️⃣ Load Lightbox JS if required
        if (!window.Lightbox) {
            await new Promise(resolve => {
                const script = document.createElement('script');
                script.src = "https://tnpg.moamalat.net:6006/js/lightbox.js";
                script.onload = resolve;
                script.onerror = resolve;
                document.head.appendChild(script);
            });
        }

        // 5️⃣ Configure Lightbox
        window.Lightbox.Checkout.configure = {
            MID: secureData.mid,
            TID: secureData.tid,
            AmountTrxn: amount,
            MerchantReference: reference,
            TrxDateTime: trxDateTime,
            SecureHash: secureData.secure_hash,
            completeCallback: (result) => {
                // Do NOT redirect immediately
                rpc('/payment/moamalat/return', {
                    ...result,
                    access_token,
                }).then((response) => {
                    if (response.result === 'success') {
                        // Delay redirect slightly to allow Lightbox to close itself
                        setTimeout(() => {
                            window.location = "/payment/status";
                        }, 60000); // 1 min delay
                    } else {
                        alert("Payment failed: " + (response.message || "Unknown error"));
                    }
                }).catch((e) => {
                    alert("Error processing payment: " + e.message);
                });
                // Return true to Lightbox to indicate handling started
                return true;
            },
            cancelCallback() {
                window.location = "/payment/status";
            },
            errorCallback() {
                window.location = "/payment/status";
            },
        };

        // 6️⃣ Launch Lightbox
        try {
            window.Lightbox.Checkout.showLightbox();
        } catch (e) {
            this._displayErrorDialog("Lightbox Error", e.toString());
        }
    },

});





// /** @odoo-module **/
// import paymentForm from '@payment/js/payment_form';
// import { rpc } from '@web/core/network/rpc';
//
// paymentForm.include({
//
//     async _prepareInlineForm(providerId, providerCode, paymentOptionId, paymentMethodCode, flow) {
//         if (providerCode !== 'moamalat_lightbox') {
//             return this._super(...arguments);
//         }
//
//         const radio = document.querySelector('input[name="o_payment_radio"]:checked');
//         if (!radio) return this._super(...arguments);
//
//         let inlineValues = {};
//         try {
//             inlineValues = JSON.parse(radio.dataset.moamalatInlineFormValues || "{}");
//         } catch {
//             inlineValues = {};
//         }
//
//         // Amount in smallest unit (fils)
//         const amountFloat = parseFloat(this.paymentContext.amount || "0");
//         const multiplier = 100;  // AED → fils
//         const amount = Math.round(amountFloat * multiplier);
//
//         // MerchantReference (10-36 chars)
//         let merchantReference = this.paymentContext.reference;
//         if (!merchantReference || merchantReference.length < 10) {
//             merchantReference = "OdooTxn" + Date.now();
//         }
//         merchantReference = merchantReference.substring(0, 36);
//
//         console.log('1111111111111111111', merchantReference);
//         // DateTimeLocalTrxn: YYMMDDHHMMSS
//         const now = new Date();
//         const trxDateTime =
//             String(now.getFullYear()).slice(2) +
//             String(now.getMonth() + 1).padStart(2, "0") +
//             String(now.getDate()).padStart(2, "0") +
//             String(now.getHours()).padStart(2, "0") +
//             String(now.getMinutes()).padStart(2, "0") +
//             String(now.getSeconds()).padStart(2, "0");
//
//         // Get secure hash from server
//         let response;
//         try {
//             response = await rpc('/payment/moamalat/get_secure_hash', {
//                 provider_id: providerId,
//                 amount: amount,
//                 merchantReference: merchantReference,
//                 trxDateTime: trxDateTime,
//             });
//         } catch (e) {
//             return this._displayErrorDialog("Moamalat Error", e.message || e);
//         }
//         console.log('22222222222222222', response);
//         if (!response || !response.secure_hash) {
//             return this._displayErrorDialog("Moamalat Error", "Invalid Secure Hash response");
//         }
//
//         // Load Lightbox script
//         if (!window.Lightbox) {
//             await new Promise((resolve) => {
//                 const script = document.createElement('script');
//                 script.src = "https://tnpg.moamalat.net:6006/js/lightbox.js";
//                 script.onload = resolve;
//                 script.onerror = resolve;
//                 document.head.appendChild(script);
//             });
//         }
//         console.log('3333333333333');
//         // Configure Lightbox
//         window.Lightbox.Checkout.configure = {
//             // MerchantId: response.mid,
//             MID: response.mid,
//             // TerminalId: response.tid,
//             TID: response.tid,
//             AmountTrxn: amount,
//             MerchantReference: merchantReference,
//             // DateTimeLocalTrxn: trxDateTime,
//             TrxDateTime: trxDateTime,
//             SecureHash: response.secure_hash,
//             completeCallback(result) {
//                 rpc('/payment/moamalat/return', result)
//                     .finally(() => window.location = "/payment/status");
//             },
//             cancelCallback() {
//                 window.location = "/payment/status";
//             },
//             errorCallback() {
//                 window.location = "/payment/status";
//             },
//         };
//         console.log('4444444444444444444');
//         // Show Lightbox
//         try {
//             console.log('555555555555555');
//             window.Lightbox.Checkout.showLightbox();
//             console.log('6666666666666666666');
//         } catch (e) {
//             this._displayErrorDialog("Moamalat Lightbox Error", e.toString());
//         }
//     },
//
// });



