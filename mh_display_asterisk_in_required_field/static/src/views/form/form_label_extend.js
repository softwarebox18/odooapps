/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { FormLabel } from "@web/views/form/form_label";
import { onMounted } from "@odoo/owl";

// Define the patch
patch(FormLabel.prototype, "mh_display_asterisk", {
    setup() {
        // Call the original setup method if it exists
        this._super.apply(this, arguments);

        // Append the asterisk with a span if the field is required
        if (this.props.fieldInfo.modifiers.required) {
            onMounted(() => {
                const label = document.querySelector(`[for="${this.props.id}"]`);
                if (label) {
                    // Append the asterisk directly into the label's innerHTML
                    label.innerHTML += ' <span class="required-asterisk">*</span>';
                }
            });
        }
    },
});

