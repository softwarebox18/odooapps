/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Many2OneField } from '@web/views/fields/many2one/many2one_field';
import { useService } from "@web/core/utils/hooks";
import { useState, onMounted } from '@odoo/owl';
import { Many2XAutocomplete, useOpenMany2XRecord } from "@web/views/fields/relational_utils";
import { _t } from "@web/core/l10n/translation";

patch(Many2OneField.prototype,{
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.state = useState({
            many2OneConfigDict: {},
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
            "many2one.field.config",
            [["model_id.model", "=", currentModel]],
            ["config_line_ids"]
        );
        if (result.length > 0) {
            const configId = result[0].id;
            const configLines = await this.orm.searchRead(
                "many2one.field.config.lines",
                [["config_id", "=", configId]],
                ["fields_id", "is_hide_create_edit", "is_hide_search_more", "search_limit", "quick_search_more_limit", "can_open"]
            );
            const many2OneConfigDictInner = {};
            for (const line of configLines) {
                const field = await this.orm.read(
                    "ir.model.fields",
                    [line.fields_id[0]],
                    ["name"]
                );
                many2OneConfigDictInner[field[0].name] = {
                    'is_hide_create_edit': line.is_hide_create_edit,
                    'search_limit': line.search_limit,
                    'quick_search_more_limit': line.quick_search_more_limit,
                    'is_hide_search_more': line.is_hide_search_more,
                    'can_open': line.can_open,
                };
            }

            this.state.many2OneConfigDict = await many2OneConfigDictInner;
        }
    },

    get Many2XAutocompleteProps() {
        const fieldName = this.props.name;
        const fieldConfig = this.state.many2OneConfigDict[fieldName] || { is_hide_create_edit: false, search_limit: 0, is_hide_search_more: false };

        const is_hide_create_edit =  fieldConfig.is_hide_create_edit ? null : function() {};
        const search_limit =  fieldConfig.search_limit > 0 ? fieldConfig.search_limit - 1 : 7;
        const quick_search_more_limit =  fieldConfig.quick_search_more_limit > 0 ? fieldConfig.quick_search_more_limit : 320;
        const is_hide_search_more =  fieldConfig.is_hide_search_more ? fieldConfig.is_hide_search_more : false;
        const canOpen =  fieldConfig.can_open ? fieldConfig.can_open : false;

        this.props.canOpen = canOpen

        return {
            ...super.Many2XAutocompleteProps,
            quickCreate: is_hide_create_edit,
            searchLimit: search_limit,
            searchMoreLimit: quick_search_more_limit,
            noSearchMore: is_hide_search_more,
            activeActions: this.activeActions,

        };
    },
});

