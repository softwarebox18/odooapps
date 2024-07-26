/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { Many2OneField, many2OneField } from "@web/views/fields/many2one/many2one_field";
import {onMounted, useState} from "@odoo/owl";
import { AutoComplete } from "@web/core/autocomplete/autocomplete";
import { Many2XAutocomplete } from "@web/views/fields/relational_utils";
import { _t } from "@web/core/l10n/translation";
import { Domain } from "@web/core/domain";

// Patch the Many2OneField component
patch(Many2XAutocomplete.prototype, {
    setup() {
        super.setup();
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
    search(name) {
        let  fields = this.state.nameSearchConfigDict

        // Always include the 'name' field in the search fields
        if (!fields.includes('name')) {
            fields.push('name');
        }
        // console.log('Domain Fields:',fields);

        // Get the dynamic custom domain
        const customDomain = this.getCustomDomain(name, fields);
        // console.log('Custom domain:', customDomain);

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

        // Log the final domain for debugging
        // console.log('Combined domain:', domain);

        //Call the ORM method with the combined domain
        return this.orm.call(this.props.resModel, "name_search", [], {
            name: name,
            operator: "ilike",
            args: this.state.finalDomain,
            limit: this.props.searchLimit + 1,
            context: this.props.context,
        });
        // return this.orm.call(this.props.resModel, "name_search", [name, domain], {
        //     limit: this.props.searchLimit + 1,
        //     context: this.props.context,
        // });
    }
});