/** @odoo-module */

import ProductScreen from 'point_of_sale.ProductScreen';
import { patch } from "@web/core/utils/patch";

// Patch the Order model to override the pay() method
patch(ProductScreen.prototype, "validate_zero_quantity_pos_order", {
    async _onClickPay() {
        // Add your custom logic before calling the original function
        const order = this.env.pos.get_order();
        // Check if there are no order lines (empty order)
        if (order.orderlines.length === 0) {
            await this.showPopup('ErrorPopup', {
                title: this.env._t("Empty Order"),
                body: this.env._t("There are no products in the order. Please add products to proceed."),
            });
            return;  // Stop further execution if no products in the order
        }

        // Check if any orderlines have zero quantity
        const zeroQuantityLines = order.orderlines.filter(line => line.quantity === 0);
        if (zeroQuantityLines.length > 0) {
            const productNames = zeroQuantityLines.map((line, index) => (index + 1) + ". " + line.product.display_name).join("\n");
            await this.showPopup('ErrorPopup', {
                title: this.env._t("Invalid Quantities"),
                body: this.env._t("The following products have 0 quantity:\n" + productNames + "\n\n Please correct the quantities to proceed."),
                body_html: true, // Enable HTML for line breaks
            });
            return;  // Stop further execution if validation fails
        }

        // Call the original _onClickPay method
        await this._super.apply(this, arguments);
    }
});

