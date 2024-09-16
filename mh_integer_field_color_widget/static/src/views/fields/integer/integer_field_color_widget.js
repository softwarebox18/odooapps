/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { Component, useState, onWillUpdateProps } from "@odoo/owl";
import { IntegerField } from "@web/views/fields/integer/integer_field";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class ColorChangingIntegerField extends IntegerField {
    setup() {
        super.setup(); // Always call the parent's setup
        this.state = useState({
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

ColorChangingIntegerField.props = {
    ...standardFieldProps,
    options: { type: Object, optional: true },
    inputType: { type: String, optional: true },  // Accepting inputType
    step: { type: Number, optional: true },       // Accepting step
    placeholder: { type: String, optional: true } // Accepting placeholder
};

ColorChangingIntegerField.defaultProps = {
    options: {
        threshold: 10,
        belowThresholdColor: 'green',
        aboveThresholdColor: 'tomato',
        belowThresholdTextColor: 'white',
        aboveThresholdTextColor: 'white',
    },
};

ColorChangingIntegerField.extractProps = ({ field, attrs }) => {
    const options = attrs.options || {};
    return {
        ...IntegerField.extractProps({ field, attrs }),
        options: {
            threshold: options.threshold || 10,  // Custom or default threshold
            belowThresholdColor: options.belowThresholdColor || 'green',  // Custom or default color for below threshold
            aboveThresholdColor: options.aboveThresholdColor || 'tomato',  // Custom or default color for above threshold
            belowThresholdTextColor: options.belowThresholdTextColor || 'white',  // Custom or default text color for below threshold
            aboveThresholdTextColor: options.aboveThresholdTextColor || 'white',  // Custom or default text color for above threshold
        },
    };
};

ColorChangingIntegerField.template = 'mh_integer_field_color_widget.ColorChangingIntegerField';
ColorChangingIntegerField.displayName = _t("Change Integer Field Color");
ColorChangingIntegerField.supportedTypes = ["integer"];
ColorChangingIntegerField.isEmpty = (record, fieldName) => record.data[fieldName] === false;

registry.category("fields").add("color_integer", ColorChangingIntegerField);
