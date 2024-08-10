/** @odoo-module **/
import { patch } from 'web.utils';
var AbstractField = require('web.AbstractField');
const { hooks } = owl;
const { onMounted } = hooks;


// Define the patch for the FieldChar component
patch(AbstractField.prototype, 'mh_display_asterisk_in_required_field.AbstractField', {
    init() {
        // Call the original init method
        this._super(...arguments);
        // Append the asterisk with a span if the field is required
        const isModifierRequired = this.attrs.modifiers && this.record.evalModifiers(this.attrs.modifiers).required;
        // const isModifierValueRequired = this.attrs.modifiersValue && this.record.evalModifiers(this.attrs.evalModifiers).required;
        // if (this.field.required || isModifierRequired || isModifierValueRequired) {
        if (this.field.required || isModifierRequired) {
            onMounted(() => {
                // Retrieve the inner HTML of the current element
                const innerHTML = this.el.innerHTML;

                // Parse the inner HTML into a document
                const parser = new DOMParser();
                const doc = parser.parseFromString(innerHTML, 'text/html');

                // Find the input element and get its ID
                const inputElement = doc.querySelector('input');
                const inputId = inputElement ? inputElement.id : this.el.id;
                if (inputId) {
                    const label = document.querySelector(`[for="${inputId}"]`);
                    if (label) {
                        // Check if the asterisk already exists in the label's innerHTML
                        if (!label.querySelector('.required-asterisk')) {
                            // Append the asterisk directly into the label's innerHTML
                            label.innerHTML += ' <span class="required-asterisk">*</span>';
                        }
                    }
                }
            });
        }
    },
});
