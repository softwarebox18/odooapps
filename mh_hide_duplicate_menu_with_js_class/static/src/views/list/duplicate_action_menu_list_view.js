/** @odoo-module */

import { registry } from "@web/core/registry";
import { listView } from '@web/views/list/list_view';
import { HideDuplicateMenuListController } from "./duplicate_action_menu_list_controller";

export const HideDuplicateMenuListView = {
    ...listView,
    Controller: HideDuplicateMenuListController,
};

registry.category("views").add("hide_duplicate_menu_list_view", HideDuplicateMenuListView);