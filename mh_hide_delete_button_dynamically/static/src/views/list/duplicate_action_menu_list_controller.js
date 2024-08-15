/** @odoo-module */

import { ListController } from '@web/views/list/list_controller';
import { useService } from "@web/core/utils/hooks";
import { onMounted, useState } from "@odoo/owl";

const originalSetupList = ListController.prototype.setup;
ListController.prototype.setup = function () {
    originalSetupList.call(this);
    this.orm = useService("orm");
    this.user = useService("user");
    this.state = useState({
        hideDeleteListMenu: false,
    });

    // Fetch configuration on component mount
    onMounted(() => {
        this.fetchConfig();
    });
};

ListController.prototype.fetchConfig = async function () {
    // console.log('Fetching config...');
    const currentModel = this.props.resModel;
    // console.log('Current model:', currentModel);
    try {
        // Check if the logged-in user has the specific group
        const hasGroup = await this.user.hasGroup('mh_hide_delete_button_dynamically.group_hide_delete_menu');
        if (hasGroup) {
            const configModel = await this.orm.searchRead(
                "hide.delete.button.config",
                [["model_id.model", "=", currentModel]],
                ["is_active"]
            );
            // console.log('ORM response:', configModel);
            if (configModel.length > 0) {
                const isActive = configModel[0].is_active;
                if (isActive) {
                    this.state.hideDeleteListMenu = true;
                }
            } else {
                this.state.hideDeleteListMenu = false;
            }
        }
    } catch (error) {
        console.error('Error fetching config:', error);
    }
};

const originalGetStaticActionMenuItemsList = ListController.prototype.getStaticActionMenuItems;
ListController.prototype.getStaticActionMenuItems = function () {
    const menuItems = originalGetStaticActionMenuItemsList.call(this);
    if (this.state.hideDeleteListMenu && menuItems.hasOwnProperty('delete')) {
        delete menuItems.delete;
    }
    return menuItems;
};

