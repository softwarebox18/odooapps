/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { Component, useState, onWillUpdateProps } from "@odoo/owl";
import { IntegerField } from "@web/views/fields/integer/integer_field";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class StarRatingIntegerWidget extends IntegerField {

    setup() {
        super.setup();
        this.maxRating = 5;  // Default maximum rating (5 stars)
        this.state = useState({
            rating: this.value || 0,  // Use the integer value as the initial rating
        });

        // Retrieve dynamic options from props or set defaults
        this.maxRating = this.props.options?.maxStars || 5;  // Dynamic number of stars
        this.filledColor = this.props.options?.filledColor || "golden";  // Default to gold for filled stars
        this.unfilledColor = this.props.options?.unfilledColor || "grey";  // Default to light grey for unfilled stars
        this.starSpacing = this.props.options?.starSpacing || 4;  // Default spacing between stars
        this.starWidth = this.props.options?.starWidth || 20;  // Default width of each star

        // Bind the method to ensure 'this' works correctly
        this.onStarClick = this.onStarClick.bind(this);
    }

    // Handle user clicking on a star
    onStarClick(starValue) {
        this.state.rating = starValue;
        this.updateRecord(starValue);  // Update the field value
    }

    get stars() {
        return Array.from({ length: this.maxRating }, (_, index) => index + 1);
    }

    get value() {
        return this.props.record.data[this.props.name];
    }
    updateRecord(newValue) {
        if (this.props.record && this.props.record.update) {
            // Update the record directly using the record's update method
            this.props.record.update({ [this.props.name]: newValue });
        }
    }
}

StarRatingIntegerWidget.props = {
    ...standardFieldProps,
    options: { type: Object, optional: true },
    inputType: { type: String, optional: true },  // Accepting inputType
    step: { type: Number, optional: true },       // Accepting step
    placeholder: { type: String, optional: true } // Accepting placeholder
};

StarRatingIntegerWidget.extractProps = ({ field, attrs }) => {
    const options = attrs.options || {};
    return {
        ...IntegerField.extractProps({ field, attrs }),
        options: {
            maxStars: options?.maxStars || 5,
            filledColor: options?.filledColor || "golden",
            unfilledColor: options?.unfilledColor || "grey",
            starSpacing: options?.starSpacing || 4,
            starWidth: options?.starWidth || 20,
        },
    };
};

StarRatingIntegerWidget.template = 'mh_integer_field_star_rating_widget.StarRatingWidget';
StarRatingIntegerWidget.displayName = _t("Star Rating Widget");
StarRatingIntegerWidget.supportedTypes = ["integer"];
StarRatingIntegerWidget.isEmpty = (record, fieldName) => record.data[fieldName] === false;

registry.category("fields").add("star_rating", StarRatingIntegerWidget);
