/** @odoo-module **/

import { SearchBarMenu } from "@web/search/search_bar_menu/search_bar_menu";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";
// Patch the component
patch(SearchBarMenu.prototype, {
    setup() {
        // Call the original setup method if it exists
        super.setup();
        this.user = useService("user");
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

