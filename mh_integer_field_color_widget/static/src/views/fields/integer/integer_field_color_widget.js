/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { Component, useState, onWillUpdateProps } from "@odoo/owl";
import { IntegerField } from "@web/views/fields/integer/integer_field";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class ColorChangingIntegerField extends IntegerField {
    static template = "mh_integer_field_color_widget.ColorChangingIntegerField"; // Make sure this matches your XML template id

    static props = {
        ...standardFieldProps,
        options: { type: Object, optional: true },
    };

    static defaultProps = {
        options: {
            threshold: 10,
            belowThresholdColor: 'green',
            aboveThresholdColor: 'tomato',
            belowThresholdTextColor: 'white',
            aboveThresholdTextColor: 'white',
        },
    };

    setup() {
        super.setup(); // Call the setup method of IntegerField
        this.state = useState({
            ...this.state,
            textColor: '',
            bgColor: '',
            className: '',
        });
        this.updateColor();
    }

    updateColor() {
        const value = this.value;
        const options = this.props.options || {};
        const threshold = options.threshold || 10;
        const belowThresholdColor = options.belowThresholdColor || 'green';
        const aboveThresholdColor = options.aboveThresholdColor || 'tomato';

        const belowThresholdTextColor = options.belowThresholdTextColor || 'white';
        const aboveThresholdTextColor = options.aboveThresholdTextColor || 'white';

        if (value <= threshold) {
            this.state.bgColor = belowThresholdColor;
            this.state.className = 'field-below-threshold';
            this.state.textColor = belowThresholdTextColor;
        } else {
            this.state.bgColor = aboveThresholdColor;
            this.state.className = 'field-above-threshold';
            this.state.textColor = aboveThresholdTextColor;
        }
    }

    get value() {
        return this.props.record.data[this.props.name] || 0;
    }

    willUpdateProps(nextProps) {
        super.willUpdateProps(nextProps);
        this.updateColor();  // Call updateColor whenever the component is re-rendetomato
    }
}
// ColorChangingIntegerField.template = 'mh_integer_field_color_widget.ColorChangingIntegerField';
export const colorChangingIntegerField = {
    component: ColorChangingIntegerField,
    displayName: _t("Change Integer Field Color"),
    supportedOptions: [
        {
            label: _t("Threshold"),
            name: "threshold",
            type: "number",
            default: 10,
            help: _t("Value at which the color changes."),
        },
        {
            label: _t("Background Color below threshold"),
            name: "belowThresholdColor",
            type: "string",
            default: "green",
            help: _t("Color to use when the value is less than or equal to the threshold."),
        },
        {
            label: _t("Background Color above threshold"),
            name: "aboveThresholdColor",
            type: "string",
            default: "tomato",
            help: _t("Color to use when the value exceeds the threshold."),
        },
        {
            label: _t("Text Color below threshold"),
            name: "belowThresholdTextColor",
            type: "string",
            default: "white",
            help: _t("Text Color to use when the value is less than or equal to the threshold."),
        },
        {
            label: _t("Text Color above threshold"),
            name: "aboveThresholdTextColor",
            type: "string",
            default: "white",
            help: _t("Text Color to use when the value exceeds the threshold."),
        },
    ],
    supportedTypes: ["integer"],
    isEmpty: (record, fieldName) => record.data[fieldName] === false,
    extractProps: ({ attrs, options }) => ({
        options: {
            threshold: options?.threshold || 10,
            belowThresholdColor: options?.belowThresholdColor || 'green',
            aboveThresholdColor: options?.aboveThresholdColor || 'tomato',
            belowThresholdTextColor: options?.belowThresholdTextColor || 'white',
            aboveThresholdTextColor: options?.aboveThresholdTextColor || 'white',
        },
        // placeholder: attrs.placeholder,
    }),
};


registry.category("fields").add("color_integer", colorChangingIntegerField);
