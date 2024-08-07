/** @odoo-module */

import { FormController } from '@web/views/form/form_controller';
import { useService } from "@web/core/utils/hooks";
import { onMounted, useState } from "@odoo/owl";

export class HideDuplicateMenuFormController extends FormController {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.user = useService("user");
        this.state = useState({
            hideDuplicateMenu: false,
        });

        // Fetch configuration on component mount
        onMounted(() => {
            this.fetchConfig();
        });
    }

    async fetchConfig() {
        const currentModel = this.props.resModel;
        try {
            // Check if the logged-in user has the specific group
            const hasGroup = await this.user.hasGroup('mh_hide_duplicate_menu_with_js_class.group_hide_duplicate_menu');
            if (hasGroup) {
                const configModel = await this.orm.searchRead(
                    "hide.duplicate.button.config",
                    [["model_id.model", "=", currentModel]],
                    ["is_active"]
                );
                if (configModel.length > 0) {
                    const isActive = configModel[0].is_active;
                    if (isActive) {
                        this.state.hideDuplicateMenu = true;
                    }
                } else {
                    this.state.hideDuplicateMenu = false;
                }
            }
        } catch (error) {
            console.error('Error fetching config:', error); // Add this line to catch and log errors
        }
    }

    getStaticActionMenuItems() {
        const menuItems = super.getStaticActionMenuItems();
        if (this.state.hideDuplicateMenu) {
            delete menuItems.duplicate;
        }
        return menuItems;
    }
}