/** @odoo-module */

import { FormController } from '@web/views/form/form_controller';
import { useService } from "@web/core/utils/hooks";
import { onMounted, useState } from "@odoo/owl";

const originalSetupForm = FormController.prototype.setup;
FormController.prototype.setup = function () {
    originalSetupForm.call(this);
    this.orm = useService("orm");
    this.user = useService("user");
    this.state = useState({
        hideDeleteFormMenu: false,
    });

    // Fetch configuration on component mount
    onMounted(() => {
        this.fetchConfig();
    });
};

FormController.prototype.fetchConfig = async function () {
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
                    this.state.hideDeleteFormMenu = true;
                }
            } else {
                this.state.hideDeleteFormMenu = false;
            }
        }
    } catch (error) {
        console.error('Error fetching config:', error);
    }
};

const originalGetStaticActionMenuItemsForm = FormController.prototype.getStaticActionMenuItems;
FormController.prototype.getStaticActionMenuItems = function () {
    const menuItems = originalGetStaticActionMenuItemsForm.call(this);
    if (this.state.hideDeleteFormMenu && menuItems.hasOwnProperty('delete')) {
        delete menuItems.delete;
    }
    return menuItems;
};

