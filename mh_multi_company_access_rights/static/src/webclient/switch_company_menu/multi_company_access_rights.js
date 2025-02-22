/** @odoo-module **/

import { SwitchCompanyMenu, SwitchCompanyItem } from "@web/webclient/switch_company_menu/switch_company_menu";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";

// Patch the SwitchCompanyMenu component
patch(SwitchCompanyItem.prototype, {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.user = useService("user");
    },


    async logIntoCompany() {

        if (this.isCompanyAllowed) {
            // Call custom Python function before switching company
            try {
                this.orm.call("res.users", "update_user_groups_for_company", [this.user.userId,this.props.company.id,]);
            } catch (error) {
                console.error("Error calling custom Python function:", error);
            }

            // Add a 500ms delay
            await new Promise(resolve => setTimeout(resolve, 500));

            // Proceed with the default company switch
            this.companySelector.switchCompany("loginto", this.props.company.id);
        }
    },

});


