/** @odoo-module **/

import { Dropdown } from "@web/core/dropdown/dropdown";
import { SearchDropdownItem } from "@web/search/search_dropdown_item/search_dropdown_item";
import { CustomFilterItem } from "@web/search/filter_menu/custom_filter_item";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";
import rpc from 'web.rpc';

// Patch the SwitchCompanyMenu component
patch(CustomFilterItem.prototype, "hide_add_custom_filter", {
    setup() {
        // Call the original setup method
        this._super(...arguments);
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

