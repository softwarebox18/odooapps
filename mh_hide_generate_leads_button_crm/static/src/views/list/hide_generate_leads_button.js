/** @odoo-module **/

import { useService } from "@web/core/utils/hooks";
import { useGenerateLeadsButton } from "@crm_iap_mine/views/generate_leads_hook";

const { onWillStart, useComponent } = owl;

export function useGenerateLeadsButtonCustom() {
    // Call the original hook
    useGenerateLeadsButton(); // Ensure this is executed to retain original functionality

    const component = useComponent();
    const user = useService("user");
    const action = useService("action");

    // Override or extend the behavior in onWillStart
    onWillStart(async () => {
        // Add your custom logic
        component.isHideGenerateLeads = await user.hasGroup("mh_hide_generate_leads_button_crm.group_hide_generate_leads");
        // console.log('Custom logic added');
        component.isSalesManager = await user.hasGroup("sales_team.group_sale_manager");
        // Add more customizations if needed
    });

    // Override or extend the onClickGenerateLead method
    component.onClickGenerateLead = () => {
        const leadType = component.props.context.default_type;

        // Custom logic before calling the original action
        // console.log("Generating lead with custom logic");

        // Original action or customized action
        action.doAction({
            name: "Generate Leads",
            type: "ir.actions.act_window",
            res_model: "crm.iap.lead.mining.request",
            target: "new",
            views: [[false, "form"]],
            context: { is_modal: true, default_lead_type: leadType },
        });

        // Add any post-action custom logic if needed
    };
}
