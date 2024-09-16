/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import {onWillStart, onMounted, useState} from "@odoo/owl";
import { Many2XAutocomplete } from "@web/views/fields/relational_utils";
import { _t } from "@web/core/l10n/translation";

// Patch the Many2OneField component
patch(Many2XAutocomplete.prototype, {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.activeSearch = false; // Track active search
        this.state = useState({
            changeLabelConfigDict: {},
            finalDomain:[]
        });
        // Fetch configuration on component mount
        onMounted(() => {
            this.fetchConfig();
        });
    },

    async fetchConfig() {
        // console.log('Entering fetchConfig'); // Log fetchConfig entry
        const currentModel = this.env.model.config.resModel;
        // console.log('Current model:', currentModel); // Log the model being used
        if (currentModel != "many2one.field.change.label.config"){
            const configModel = await this.orm.searchRead(
            "many2one.field.change.label.config",
            [["model_id.model", "=", currentModel]],
            ["is_active","config_line_ids"]
            );
            // console.log('Config result:', result); // Log the result of the first ORM call

            if (configModel.length > 0) {
                const configId = configModel[0].id;
                // console.log('Config ID:', configId,configModel[0].is_active); // Log the config ID
                if (configModel[0].is_active) {
                    const configLines = await this.orm.searchRead(
                        "many2one.field.change.label.config.lines",
                        [["config_id", "=", configId]],
                        ["fields_id","create_label", "create_and_edit", "search_more_label", "start_typing_label", "no_record_label"]
                    );
                    // console.log('Config lines:', configLines); // Log the config lines

                    const changeLabelConfigDictInner = {};
                    for (const line of configLines) {
                        const field = await this.orm.read(
                            "ir.model.fields",
                            [line.fields_id[0]],
                            ["name"]
                        );
                        // console.log('Field name:', field[0].name); // Log each field name
                        changeLabelConfigDictInner[field[0].name] = {
                            'create_label': line.create_label,
                            'create_and_edit': line.create_and_edit,
                            'search_more_label': line.search_more_label,
                            'start_typing_label': line.start_typing_label,
                            'no_record_label': line.no_record_label,
                        };
                    }

                    // Update the state with the configuration
                    this.state.changeLabelConfigDict = changeLabelConfigDictInner;
                    // console.log('Updated Config Dict:', this.state.changeLabelConfigDict); // Log the updated state
                }else{
                    this.state.changeLabelConfigDict;
                }
            }
        }

    },

    async loadOptionsSource(request) {
        if (this.lastProm) {
            this.activeSearch = false;
        }
        // await this.fetchConfig();
        let create_label = "Create";
        let create_and_edit = "Create and edit...";
        let search_more_label = "Search More...";
        let start_typing_label = "Start typing...";
        let no_record_label = "No records";
        if (Object.keys(this.state.changeLabelConfigDict).length != 0) {
            let fieldName = this.props.id.replace(/_\d+$/, "");
            if (fieldName in this.state.changeLabelConfigDict) {
                const option_label = this.state.changeLabelConfigDict[fieldName]
                create_label = option_label['create_label'];
                create_and_edit = option_label['create_and_edit'];
                search_more_label = option_label['search_more_label'];
                start_typing_label = option_label['start_typing_label'];
                no_record_label = option_label['no_record_label'];
            }

        }



        this.lastProm = this.search(request);
        const records = await this.lastProm;
        const options = records.map((result) => this.mapRecordToOption(result));

        if (this.props.quickCreate && request.length) {
            options.push({
                label: _t('"%s" "%s"', create_label, request),
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
                label: _t(search_more_label),
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
                label: _t(start_typing_label),
                classList: "o_m2o_start_typing",
                unselectable: true,
            });
        }

        if (request.length && canCreateEdit) {
            const context = this.getCreationContext(request);
            options.push({
                label: _t(create_and_edit), // original its Create and edit...
                classList: "o_m2o_dropdown_option o_m2o_dropdown_option_create_edit",
                action: () => this.openMany2X({ context }),
            });
        }

        if (!records.length && !this.activeActions.create) {
            options.push({
                label: _t(no_record_label),
                classList: "o_m2o_no_result",
                unselectable: true,
            });
        }

        return options;
    },

    search(name) {
        // Mark search as active
        this.activeSearch = true;
        // Get the existing domain
        const existingDomain = this.props.getDomain();
        // console.log('Existing domain:', customDomain);

        // Combine existing domain with custom domain
        let domain = [];
        domain = [...existingDomain];
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

            // Process the results to include phone number
            const records = results.map(result => {
                const [id, displayName] = result;
                return [id, displayName];
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


});