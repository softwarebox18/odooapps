/** @odoo-module **/

import { SwitchCompanyMenu, SwitchCompanyItem } from "@web/webclient/switch_company_menu/switch_company_menu";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";

// Patch the SwitchCompanyMenu component
patch(SwitchCompanyMenu.prototype, "company_select_unselect", {
    setup() {
        // Call the original setup method
        this._super(...arguments);
        this.toggleSelectAllCompanies = this.toggleSelectAllCompanies.bind(this);
        this.companyService = useService('company');  // Use company service
        // console.log('Company Service:', this.companyService);
    },

    toggleSelectAllCompanies() {
        // Retrieve all available company IDs except the current company
        const companyIds = Object.keys(this.companyService.availableCompanies).filter(
            companyId => parseInt(companyId) !== this.companyService.currentCompanyId
        );
        // console.log('Non-default Company IDs:', companyIds);

        // Check if all other companies are selected (current company is always selected)
        const allOtherSelected = companyIds.every(companyId => this.companyService.allowedCompanyIds.includes(parseInt(companyId)));
        // console.log('Are all other companies selected?', allOtherSelected);

        if (allOtherSelected) {
            // Deselect all other companies (keep the default one selected)
            companyIds.forEach(companyId => {
                this.toggleCompany(parseInt(companyId));
            });
        } else {
            // Select all other companies (keep the default one selected)
            companyIds.forEach(companyId => {
                if (!this.companyService.allowedCompanyIds.includes(parseInt(companyId))) {
                    this.toggleCompany(parseInt(companyId));
                }
            });
        }
    },
});



