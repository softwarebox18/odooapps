/** @odoo-module **/

import { ExportAll as OriginalExportAll } from "@web/views/list/export_all/export_all";
import { registry } from "@web/core/registry";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import {onMounted, useState} from "@odoo/owl";


patch(OriginalExportAll.prototype, {
    setup() {
        // Call the original setup method
        super.setup();
        // Initialize state
        this.state = useState({
            hideExportAllListButton: false,
        });
        // Fetch configuration on component mount
        this.fetchConfig();

    },

    async fetchConfig() {
        this.orm = useService("orm");
        this.user = useService("user");
        // this.hideExportAllListButton = false; // Default value

        // Check for user group permissions
        const hasExportAllGroup = await this.user.hasGroup('mh_all_in_one_hide_action_menu.group_hide_export_all_button');

        if (hasExportAllGroup) {
            const currentModel = this.env.searchModel.resModel;
            // console.log('currentModel',currentModel);
            try {
                const configModel = await this.orm.searchRead(
                    "hide.action.menu.button.config",
                    [["model_id.model", "=", currentModel]],
                    ["is_active"]
                );

                if (configModel.length > 0) {
                    if (hasExportAllGroup) {
                        this.state.hideExportAllListButton = configModel[0].is_active;
                    }
                }
            } catch (error) {
                console.error('Error fetching configuration:', error);
            }
        }
    }

});



