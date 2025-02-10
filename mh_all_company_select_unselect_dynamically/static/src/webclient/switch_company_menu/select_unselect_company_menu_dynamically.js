/** @odoo-module **/

import { SwitchCompanyMenu, SwitchCompanyItem } from "@web/webclient/switch_company_menu/switch_company_menu";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { patch } from "@web/core/utils/patch";

// Patch the SwitchCompanyMenu component
patch(SwitchCompanyMenu.prototype, {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.applyDefaultCompanySelection();
    },

    async applyDefaultCompanySelection() {
        const param = await this.orm.call("ir.config_parameter", "get_param", [
                "mh_all_company_select_unselect_dynamically.is_allowed_companies",
            ]);

        const isAllowedCompanies = param === "True"; // Convert string to boolean
        const companyIds = Object.keys(this.companyService.allowedCompanies).map(id => parseInt(id));
        const defaultCompanyId = this.companyService.currentCompanyId;
        const allSelected = companyIds.every(companyId => this.companySelector.isCompanySelected(parseInt(companyId)));

        if (isAllowedCompanies) {
            // Select all companies by default
            companyIds.forEach(companyId => {
                if (!this.companySelector.isCompanySelected(companyId)) {
                    this.companySelector.switchCompany("toggle", companyId);
                }
            });
        }
        else{
            if (allSelected) {
                // Deselect all companies
                companyIds.forEach(companyId => {
                    this.companySelector.switchCompany("toggle", parseInt(companyId));
                });
            }
        }
    }
});

