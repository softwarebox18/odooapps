/** @odoo-module **/

import { SearchBarMenu } from "@web/search/search_bar_menu/search_bar_menu";
import { patch } from "@web/core/utils/patch";
import { user } from "@web/core/user";
// Patch the component
patch(SearchBarMenu.prototype, {
    setup() {
        // Call the original setup method if it exists
        super.setup();
        this.user = user;
        this.showCustomFilter = false;  // Default: Hidden

        this.checkUserGroup();
    },

    async checkUserGroup() {
        const is_hide_add_custom_filter = await this.user.hasGroup("mh_hide_add_custom_filter.group_hide_add_custom_filter");

        if (is_hide_add_custom_filter) {
            this.showCustomFilter = true;  // Modify with your group
            this.render();  // Re-render to apply changes
        }
    },

});

