/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";
import { IntegerField } from "@web/views/fields/integer/integer_field";
// import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class StepInputWidget extends IntegerField {
    static template = "mh_integer_field_step_input_widget.StepInputWidget";

    // static props = {
    //     ...standardFieldProps,
    //     options: { type: Object, optional: true },
    // };

    setup() {
        super.setup();
        this.state = useState({
            value: this.value || 0,
        });
    }

    refresh() {
        this.state.value = 0;
        this.updateFieldValue();
    }

    increment() {
        const step = this.props.options?.step || 1;
        const maxValue = this.props.options?.max_value ?? Infinity; // Handle max_value
        if (this.state.value + step <= maxValue) {
            this.state.value += step;
            this.updateFieldValue();
        }
    }

    decrement() {
        const step = this.props.options?.step || 1;
        const minValue = this.props.options?.min_value ?? -Infinity; // Handle min_value
        if (this.state.value - step >= minValue) {
            this.state.value -= step;
            this.updateFieldValue();
        }
    }

    updateFieldValue() {
        if (this.props.record && this.props.record.update) {
            // Update the record directly using the record's update method
            this.props.record.update({ [this.props.name]: this.state.value });
        }
    }

    get value() {
        return this.props.record.data[this.props.name];
    }
}

// Register the component
export const stepInputWidget = {
    component: StepInputWidget,
    displayName: _t("Step Input Widget"),
    supportedTypes: ["integer"],
    isEmpty: (record, fieldName) => record.data[fieldName] === false,
    extractProps: ({ attrs, options }) => ({
        options: {
            step: options?.step || 1,
            min_value: options?.min_value ?? -Infinity, // Default to no minimum limit
            max_value: options?.max_value ?? Infinity,  // Default to no maximum limit
        },
    }),
};

registry.category("fields").add("step_input", stepInputWidget);
