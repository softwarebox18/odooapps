/** @odoo-module **/

import { crmKanbanView } from "@crm/views/crm_kanban/crm_kanban_view";
import { patch } from "@web/core/utils/patch";
import { useGenerateLeadsButtonCustom } from "@mh_hide_generate_leads_button_crm/views/list/hide_generate_leads_button"; // Adjust the path to your custom useGenerateLeadsButton
import { LeadMiningRequestListController } from "@crm_iap_mine/views/generate_leads_views";


patch(LeadMiningRequestListController.prototype, "crm_iap_lead_mining_request_list_custom", {
    setup() {
        this._super(...arguments);
        useGenerateLeadsButtonCustom();
    },
});

// Extend the existing patch
patch(crmKanbanView.Controller.prototype, "crm_iap_lead_mining_request_kanban_custom", {
    setup() {
        this._super(...arguments); // Call the original setup method
        useGenerateLeadsButtonCustom(); // Use your custom hook
    },
});