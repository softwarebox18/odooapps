/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
const { useRef, onPatched, onMounted, useState } = owl;
import { Many2XAutocomplete } from "@web/views/fields/relational_utils";
import { sprintf } from "@web/core/utils/strings";

// Patch the Many2OneField component
patch(Many2XAutocomplete.prototype, 'dynamic_name_search_patch', {
    setup() {
        this._super.apply(this, arguments);
        this.orm = useService("orm");
        this.state = useState({
            nameSearchConfigDict: [],
            finalDomain:[]
        });

        // Fetch configuration on component mount
        onMounted(() => {
            this.fetchConfig();
        });
    },
    getCustomDomain(name, fields) {
        if (fields.length === 0) {
            return [];
        }

        // Create an array to hold the domain conditions
        const domainConditions = fields.map(field => [field, 'ilike', name]);
        // If there is only one condition, return it directly
        if (domainConditions.length === 1) {
            return domainConditions;
        }

        // If there are multiple conditions, combine them with 'OR'
        let combinedDomain = [];
        for (let i = 0; i < domainConditions.length - 1; i++) {
            combinedDomain.push('|');
        }
        combinedDomain.push(...domainConditions);

        return combinedDomain;
    },
    async fetchConfig() {
        const currentModel = this.props.resModel;
        const configModel = await this.orm.searchRead(
            "many2one.name.search.config",
            [["model_id.model", "=", currentModel]],
            ["is_active","fields_ids"]
        );
        if (configModel.length > 0) {
            const configId = configModel[0].id;
            if (configModel[0].is_active) {
                const configFields = await this.orm.searchRead(
                    "ir.model.fields",
                    [["id", "in", configModel[0].fields_ids]],
                    ["name"]
                );
                // Use map to extract the 'name' property from each object
                const fieldNames = configFields.map(field => field.name);
                this.state.nameSearchConfigDict = await fieldNames;
            }else{
                this.state.nameSearchConfigDict = [];
            }
        }else {
            this.state.nameSearchConfigDict = [];
        }
    },
    /**
     * @override
     */

    async loadOptionsSource(request) {
        if (this.lastProm) {
            this.lastProm.abort(false);
        }
        let fields = this.state.nameSearchConfigDict;

        // Always include the 'name' field in the search fields
        if (!fields.includes('name')) {
            fields.push('name');
        }

        // Get the dynamic custom domain
        const customDomain = this.getCustomDomain(request, fields);

        // Get the existing domain
        const existingDomain = this.props.getDomain();

        // Combine existing domain with custom domain
        let domain = [];
        if (existingDomain.length && customDomain.length) {
            domain = [...existingDomain, ...customDomain];
        } else if (existingDomain.length) {
            domain = [...existingDomain];
        } else {
            domain = customDomain;
        }
        this.state.finalDomain = domain;
        // Call the ORM method with the combined domain
        this.lastProm = this.orm.call(this.props.resModel, "name_search", [], {
            name: request,
            operator: "ilike",
            args: this.state.finalDomain,
            limit: this.props.searchLimit + 1,
            context: this.props.context,
        });

        const records = await this.lastProm;

        const options = records.map((result) => ({
            value: result[0],
            label: result[1].split("\n")[0],
        }));

        if (this.props.quickCreate && request.length) {
            options.push({
                label: sprintf(this.env._t(`Create "%s"`), request),
                classList: "o_m2o_dropdown_option o_m2o_dropdown_option_create",
                action: async (params) => {
                    try {
                        await this.props.quickCreate(request, params);
                    } catch (e) {
                        if (
                            e &&
                            e.name === "RPC_ERROR" &&
                            e.exceptionName === "odoo.exceptions.ValidationError"
                        ) {
                            const context = this.getCreationContext(request);
                            return this.openMany2X({ context });
                        }
                        // Compatibility with legacy code
                        if (
                            e &&
                            e.message &&
                            e.message.name === "RPC_ERROR" &&
                            e.message.exceptionName === "odoo.exceptions.ValidationError"
                        ) {
                            // The event.preventDefault() is necessary because we still use the legacy
                            e.event.preventDefault();
                            const context = this.getCreationContext(request);
                            return this.openMany2X({ context });
                        }
                        throw e;
                    }
                },
            });
        }

        if (!this.props.noSearchMore && this.props.searchLimit < records.length) {
            options.push({
                label: this.env._t("Search More..."),
                action: this.onSearchMore.bind(this, request),
                classList: "o_m2o_dropdown_option o_m2o_dropdown_option_search_more",
            });
        }

        const canCreateEdit =
            "createEdit" in this.activeActions
                ? this.activeActions.createEdit
                : this.activeActions.create;
        if (!request.length && !this.props.value && (this.props.quickCreate || canCreateEdit)) {
            options.push({
                label: this.env._t("Start typing..."),
                classList: "o_m2o_start_typing",
                unselectable: true,
            });
        }

        if (request.length && canCreateEdit) {
            const context = this.getCreationContext(request);
            options.push({
                label: this.env._t("Create and edit..."),
                classList: "o_m2o_dropdown_option o_m2o_dropdown_option_create_edit",
                action: () => this.openMany2X({ context }),
            });
        }

        if (!records.length && !this.activeActions.create) {
            options.push({
                label: this.env._t("No records"),
                classList: "o_m2o_no_result",
                unselectable: true,
            });
        }

        return options;
    }
});