/** @odoo-module **/

import { SwitchCompanyMenu, SwitchCompanyItem } from "@web/webclient/switch_company_menu/switch_company_menu";

import { registry } from "@web/core/registry";
import { patch } from "@web/core/utils/patch";

// Patch the SwitchCompanyMenu component
patch(SwitchCompanyMenu.prototype, {
    setup() {
        // Call the original setup method if it exists
        super.setup();
        this.toggleSelectAllCompanies = this.toggleSelectAllCompanies.bind(this);
    },

    toggleSelectAllCompanies() {
        const companyIds = Object.keys(this.companyService.allowedCompanies);
        const allSelected = companyIds.every(companyId => this.companySelector.isCompanySelected(parseInt(companyId)));

        if (allSelected) {
            // Deselect all companies
            companyIds.forEach(companyId => {
                this.companySelector.switchCompany("toggle", parseInt(companyId));
            });
        } else {
            // Select all companies
            companyIds.forEach(companyId => {
                if (!this.companySelector.isCompanySelected(parseInt(companyId))) {
                    this.companySelector.switchCompany("toggle", parseInt(companyId));
                }
            });
        }
        this.companySelector._apply();
    }
});



