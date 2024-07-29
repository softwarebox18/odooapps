/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import {onMounted, useState} from "@odoo/owl";
import { Many2XAutocomplete } from "@web/views/fields/relational_utils";
import { _t } from "@web/core/l10n/translation";

// Patch the Many2OneField component
patch(Many2XAutocomplete.prototype, {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.activeSearch = false; // Track active search
        this.state = useState({
            nameSearchGetConfigDict: [],
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
            "many2one.name.search.and.get.config",
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
                const valueFields = await this.orm.searchRead(
                    currentModel,
                    [],
                    fieldNames
                );
                this.state.nameSearchGetConfigDict = await valueFields;
            }else{
                this.state.nameSearchGetConfigDict = [];
            }
        }else {
            this.state.nameSearchGetConfigDict = [];
        }
    },
    /**
     * @override
     */

    modifyText(text, customText) {
        // Split the text at the first newline character
        const parts = text.split(/\n/);

        // If customText is not provided or is empty, just return the original text
        if (!customText) {
            return text;
        }

        // Ensure there are at least two parts
        if (parts.length < 2) {
            // If there's no newline, just return the original text with custom text appended
            return text + ' - ' + customText;
        }

        // Get the part before the first newline and the part after
        const beforeFirstNewline = parts[0];
        const remainingText = parts.slice(1).join('\n');

        // Concatenate custom text after the part before the newline using a dash
        return beforeFirstNewline + ' - ' + customText +'\n'+ remainingText;

    },

    search(name) {
        // Mark search as active
        this.activeSearch = true;

        // Construct a custom domain based on the name and configured fields
        const fields = this.state.nameSearchGetConfigDict.length ? Object.keys(this.state.nameSearchGetConfigDict[0]).filter(key => key !== 'id') : [];

        // Always include the 'name' field in the search fields
        if (!fields.includes('name')) {
            fields.push('name');
        }
        const customDomain = this.getCustomDomain(name, fields);

        // Get the existing domain
        const existingDomain = this.props.getDomain();
        // console.log('Existing domain:', customDomain);

        // Combine existing domain with custom domain
        let domain = [];
        if (existingDomain.length && customDomain.length) {
            domain = [...existingDomain, ...customDomain];
        } else if (existingDomain.length) {
            domain = [...existingDomain];
        } else {
            domain = customDomain;
        }
        this.state.finalDomain = domain

        // Perform the search request
        this.lastProm = this.orm.call(this.props.resModel, "name_search", [], {
            name: name,
            operator: "ilike",
            args: this.state.finalDomain,
            // args: this.props.getDomain(),
            limit: this.props.searchLimit + 1,
            context: this.props.context,
        }).then((results) => {
            // Ignore results if search was aborted
            if (!this.activeSearch) return [];

            // If nameSearchGetConfigDict is empty, return default results
            if (!this.state.nameSearchGetConfigDict.length) {
                return results;
            }

            // Process the results to include phone number
            const records = results.map(result => {
                const [id, displayName] = result;
                const config = this.state.nameSearchGetConfigDict.find(config => config.id === id);
                // Concatenate all fields except 'id' with a dash
                const customTexts = Object.entries(config || {})
                    .filter(([key]) => key !== 'id') // Exclude 'id'
                    .map(([key, value]) => value) // Extract values
                    .filter(value => value) // Filter out empty values
                    .join(' - '); // Concatenate with dash
                const customizedDisplayName = this.modifyText(displayName, customTexts);
                const customDisplayName = customizedDisplayName ? customizedDisplayName : displayName;
                return [id, customDisplayName];
            });

            return records;
        }).catch((error) => {
            // Handle errors appropriately
            if (!this.activeSearch) return []; // Ignore if search was aborted

            throw error; // Re-throw other errors
        }).finally(() => {
            // Mark search as inactive
            this.activeSearch = false;
        });

        return this.lastProm;
    },

    async loadOptionsSource(request) {
        if (this.lastProm) {
            this.activeSearch = false;
        }

        this.lastProm = this.search(request);
        const records = await this.lastProm;
        const options = records.map((result) => this.mapRecordToOption(result));

        if (this.props.quickCreate && request.length) {
            options.push({
                label: _t('Create "%s"', request),
                classList: "o_m2o_dropdown_option o_m2o_dropdown_option_create",
                action: async (params) => {
                    try {
                        await this.props.quickCreate(request, params);
                    } catch (e) {
                        if (
                            e instanceof RPCError &&
                            e.exceptionName === "odoo.exceptions.ValidationError"
                        ) {
                            const context = this.getCreationContext(request);
                            return this.openMany2X({ context });
                        }
                        throw e;
                    }
                },
            });
        }

        if (!this.props.noSearchMore && records.length > 0) {
            options.push({
                label: _t("Search More..."),
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
                label: _t("Start typing..."),
                classList: "o_m2o_start_typing",
                unselectable: true,
            });
        }

        if (request.length && canCreateEdit) {
            const context = this.getCreationContext(request);
            options.push({
                label: _t("Create and edit..."),
                classList: "o_m2o_dropdown_option o_m2o_dropdown_option_create_edit",
                action: () => this.openMany2X({ context }),
            });
        }

        if (!records.length && !this.activeActions.create) {
            options.push({
                label: _t("No records"),
                classList: "o_m2o_no_result",
                unselectable: true,
            });
        }

        return options;
    },
});