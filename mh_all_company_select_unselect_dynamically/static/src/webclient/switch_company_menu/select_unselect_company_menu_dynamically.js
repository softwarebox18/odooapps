/** @odoo-module **/

import { SwitchCompanyMenu, SwitchCompanyItem } from "@web/webclient/switch_company_menu/switch_company_menu";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";
import rpc from 'web.rpc';

// Patch the SwitchCompanyMenu component
patch(SwitchCompanyMenu.prototype, "company_select_unselect_dynamically", {
    setup() {
        // Call the original setup method
        this._super(...arguments);
        this.applyDefaultCompanySelection();
    },

    async applyDefaultCompanySelection() {
        const param = await rpc.query({model: 'ir.config_parameter', method: 'get_param', args: ["mh_all_company_select_unselect_dynamically.is_allowed_companies"],});

        const isAllowedCompanies = param === "True"; // Convert string to boolean
        // Retrieve all available company IDs except the current company
        const companyIds = Object.keys(this.companyService.availableCompanies).filter(
            companyId => parseInt(companyId) !== this.companyService.currentCompanyId
        );

        // Check if all other companies are selected (current company is always selected)
        const allOtherSelected = companyIds.every(companyId => this.companyService.allowedCompanyIds.includes(parseInt(companyId)));

        if (isAllowedCompanies) {

            // Select all other companies (keep the default one selected)
            companyIds.forEach(companyId => {
                if (!this.companyService.allowedCompanyIds.includes(parseInt(companyId))) {
                    this.toggleCompany(parseInt(companyId));
                }
            });
        }
        else{
            if (allOtherSelected) {
                // Deselect all other companies (keep the default one selected)
                companyIds.forEach(companyId => {
                    this.toggleCompany(parseInt(companyId));
                });
            }
        }
    }
});

