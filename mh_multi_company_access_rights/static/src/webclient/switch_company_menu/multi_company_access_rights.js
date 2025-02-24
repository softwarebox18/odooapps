/** @odoo-module **/

import { SwitchCompanyMenu, SwitchCompanyItem } from "@web/webclient/switch_company_menu/switch_company_menu";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";
import rpc from 'web.rpc';
import { browser } from "@web/core/browser/browser";

// Patch the SwitchCompanyMenu component
patch(SwitchCompanyMenu.prototype, "multi_company_access_rights", {
    setup() {
        // Call the original setup method
        this._super(...arguments);
        this.user = useService("user");
    },


    async logIntoCompany(companyId) {
        // Call custom Python function before switching company
        try {
            await rpc.query({model: 'res.users', method: 'update_user_groups_for_company', args: [this.user.userId,companyId,],});
        } catch (error) {
            console.error("Error calling custom Python function:", error);
        }

        // Add a 500ms delay
        // await new Promise(resolve => setTimeout(resolve, 500));

        browser.clearTimeout(this.toggleTimer);
        this.companyService.setCompanies("loginto", companyId);
    },

});


