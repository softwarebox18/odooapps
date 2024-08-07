// /** @odoo-module */
//
// import { FormController } from '@web/views/form/form_controller';
// import { useService } from "@web/core/utils/hooks";
// import { onMounted, useState } from "@odoo/owl";
//
// const originalSetup = FormController.prototype.setup;
// FormController.prototype.setup = function () {
//     originalSetup.call(this);
//     this.action = useService("action");
//     this.orm = useService("orm");
//     this.dialogService = useService("dialog");
//     this.user = useService("user");
//     this.state = useState({
//         hideDuplicateMenu: false,
//     });
//
//     // Fetch configuration on component mount
//     onMounted(() => {
//         this.fetchConfig();
//     });
// };
//
// FormController.prototype.fetchConfig = async function () {
//     console.log('Fetching config...');
//     const currentModel = this.props.resModel;
//     console.log('Current model:', currentModel);
//     try {
//         // Check if the logged-in user has the specific group
//         const hasGroup = await this.user.hasGroup('mh_hide_duplicate_button_dynamically.group_hide_duplicate_menu');
//         if (hasGroup) {
//             const configModel = await this.orm.searchRead(
//                 "hide.duplicate.button.config",
//                 [["model_id.model", "=", currentModel]],
//                 ["is_active"]
//             );
//             console.log('ORM response:', configModel);
//             if (configModel.length > 0) {
//                 const isActive = configModel[0].is_active;
//                 if (isActive) {
//                     this.state.hideDuplicateMenu = true;
//                 }
//             } else {
//                 this.state.hideDuplicateMenu = false;
//             }
//         }
//     } catch (error) {
//         console.error('Error fetching config:', error);
//     }
// };
//
// const originalGetStaticActionMenuItems = FormController.prototype.getStaticActionMenuItems;
// FormController.prototype.getStaticActionMenuItems = function () {
//     console.log('1111111111111111', this.state.hideDuplicateMenu);
//     const menuItems = originalGetStaticActionMenuItems.call(this);
//     console.log('222222222222222', menuItems);
//     if (this.state.hideDuplicateMenu) {
//         delete menuItems.duplicate;
//     }
//     return menuItems;
// };




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
        console.log('1111111111111111', this.state.hideDuplicateMenuList);
        const menuItems = super.getStaticActionMenuItems();
        console.log('222222222222222',menuItems);
        if (this.state.hideDuplicateMenuList) {
            delete menuItems.duplicate;
        }
        return menuItems;
    }
}

// // Register the custom form controller
// registry.category("controllers").add("mudassir_form_controller", HideDuplicateMenuListController);
//
// // Register a new view type that uses the custom form controller
// const mudassirFormView = {
//     ...formView,
//     Controller: HideDuplicateMenuListController,
// };
//
// // Register the new view
// registry.category("views").add("mudassir_form_view", mudassirFormView);

