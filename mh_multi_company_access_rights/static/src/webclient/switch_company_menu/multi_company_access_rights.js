/** @odoo-module **/

import { SwitchCompanyMenu, SwitchCompanyItem } from "@web/webclient/switch_company_menu/switch_company_item";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";
import { symmetricalDifference } from "@web/core/utils/arrays";
import { user } from "@web/core/user";

// Patch the SwitchCompanyMenu component
patch(SwitchCompanyItem.prototype, {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.userId = user.userId;
        // console.log('11111111111111111',this)
    },

    async logIntoCompany() {
        if (this.isCompanyAllowed) {
            // Call custom Python function before switching company
            try {
                // console.log('2222222222222',this.userId,this.props.company.id)
                await this.orm.call("res.users", "update_user_groups_for_company", [this.userId,this.props.company.id,]);
            } catch (error) {
                console.error("Error calling custom Python function:", error);
            }

            // Proceed with the default company switch
            this.companySelector.switchCompany("loginto", this.props.company.id);
        }
    },
});


