/** @odoo-module */

import { registry } from "@web/core/registry";
import { formView } from '@web/views/form/form_view';
import { HideDuplicateMenuFormController } from "./duplicate_action_menu_form_controller";

export const HideDuplicateMenuFormView = {
    ...formView,
    Controller: HideDuplicateMenuFormController,
};

registry.category("views").add("hide_duplicate_menu_form_view", HideDuplicateMenuFormView);