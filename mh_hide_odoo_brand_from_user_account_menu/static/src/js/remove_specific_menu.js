/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { registry } from "@web/core/registry";
import { UserMenu } from "@web/webclient/user_menu/user_menu";

// Define the patch
patch(UserMenu.prototype, "mh_hide_odoo_brand_from_user_account_menu", {
    setup() {
        // Call the original setup method if it exists
        this._super.apply(this, arguments);
        // Remove specific menu items from the registry
        const categoriesToRemoveFrom = ["user_menuitems"]; // Add category names here
        const itemsToRemove = ["documentation", "support", "shortcuts", "odoo_account"]; // Add item IDs here

        categoriesToRemoveFrom.forEach(category => {
            itemsToRemove.forEach(itemId => {
                registry.category(category).remove(itemId);
            });
        });
    },
});



// /** @odoo-module **/
// import { patch } from "@web/core/utils/patch";
// import { registry } from "@web/core/registry";
// import { UserMenu } from "@web/webclient/user_menu/user_menu";
//
// // Define the patch
// patch(UserMenu.prototype, {
//     setup() {
//         // Call the original setup method if it exists
//         super.setup();
//         // Remove specific menu items from the registry
//         const categoriesToRemoveFrom = ["user_menuitems"]; // Add category names here
//         const itemsToRemove = ["documentation","support","shortcuts","odoo_account"]; // Add item IDs here
//
//         categoriesToRemoveFrom.forEach(category => {
//             itemsToRemove.forEach(itemId => {
//                 registry.category(category).remove(itemId);
//             });
//         });
//     },
// });
//
