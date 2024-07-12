/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Many2OneField } from "@web/views/fields/many2one/many2one_field";
import { useService } from "@web/core/utils/hooks";
const { useRef, onPatched, onMounted, useState } = owl;

patch(Many2OneField.prototype, 'dynamic_disable_quick_create_patch', {
    setup() {
        this._super.apply(this, arguments);
        this.orm = useService("orm");
        this.state = useState({
            disableCreateEditConfig: {},
        });
        // Ensure activeActions and other props are initialized
        this.activeActions = this.activeActions || {};
        this.many2oneProps = this.many2oneProps || {};
        // Fetch configuration on component mount
        onMounted(() => {
            this.fetchConfig();
        });
    },

    async fetchConfig() {
        const currentModel = this.props.record.resModel;
        const result = await this.orm.searchRead(
            "disable.quick.create.edit.config",
            [["model_id.model", "=", currentModel]],
            ["model_id", "fields_ids"]
        );
        if (result.length > 0) {
            const fieldIds = result[0].fields_ids;
            const fieldNames = await this.orm.searchRead(
                "ir.model.fields",
                [["id", "in", fieldIds]],
                ["name"]
            );
            const disableCreateEditConfig = {};
            for (const field of fieldNames) {
                disableCreateEditConfig[field.name] = true;
            }

            this.state.disableCreateEditConfig = disableCreateEditConfig;
        }
    },

    get Many2XAutocompleteProps() {
        const fieldName = this.props.name;
        const disableCreateEdit = this.state.disableCreateEditConfig[fieldName];
        // Log for debugging
        // console.log(`Field: ${fieldName}, Disable Quick Create: ${disableCreateEdit}`);

        return {
            ...this._super.apply(this, arguments),
            quickCreate: disableCreateEdit ? null : function() {},
            activeActions: this.activeActions,
        };
    }
});
