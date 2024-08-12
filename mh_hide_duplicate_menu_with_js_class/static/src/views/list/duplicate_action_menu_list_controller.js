/** @odoo-module */

import { ListController } from '@web/views/list/list_controller';
import { useService } from "@web/core/utils/hooks";
import { onMounted, useState } from "@odoo/owl";

export class HideDuplicateMenuListController extends ListController {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.user = useService("user");
        this.state = useState({
            hideDuplicateMenuList: false,
        });

        // Fetch configuration on component mount
        onMounted(() => {
            this.fetchConfig();
        });
    }

    async fetchConfig() {
        console.log('Fetching config...'); // Add this line
        const currentModel = this.props.resModel;
        console.log('Current model:', currentModel); // Add this line
        try {
            // Check if the logged-in user has the specific group
            const hasGroup = await this.user.hasGroup('mh_hide_duplicate_menu_with_js_class.group_hide_duplicate_menu');
            if (hasGroup) {
                const configModel = await this.orm.searchRead(
                    "hide.duplicate.button.config",
                    [["model_id.model", "=", currentModel]],
                    ["is_active"]
                );
                console.log('ORM response:', configModel); // Add this line
                if (configModel.length > 0) {
                    const isActive = configModel[0].is_active;
                    if (isActive) {
                        this.state.hideDuplicateMenuList = true;
                    }
                } else {
                    this.state.hideDuplicateMenuList = false;
                }
            }
        } catch (error) {
            console.error('Error fetching config:', error); // Add this line to catch and log errors
        }
    }

    getStaticActionMenuItems() {
        const menuItems = super.getStaticActionMenuItems();
        if (this.state.hideDuplicateMenuList) {
            delete menuItems.duplicate;
        }
        return menuItems;
    }
}