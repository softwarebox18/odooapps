/** @odoo-module */

import { ListController } from '@web/views/list/list_controller';
import { useService } from "@web/core/utils/hooks";
import { onMounted, useState } from "@odoo/owl";

const originalSetupList = ListController.prototype.setup;
ListController.prototype.setup = function () {
    originalSetupList.call(this);
    this.orm = useService("orm");
    this.user = useService("user");
    this.state = useState({
        hideDeleteListMenu: false,
        hideDuplicateListMenu: false,
        hideExportListMenu: false,
        hideArchiveListMenu: false,
        hideUnarchiveListMenu: false,
    });

    // Fetch configuration on component mount
    onMounted(() => {
        this.fetchConfig();
    });
};

ListController.prototype.fetchConfig = async function () {
    // console.log('Fetching config...');
    try {
        // Check if the logged-in user has the specific group
        const hasDeleteGroup = await this.user.hasGroup('mh_all_in_one_hide_action_menu.group_hide_delete_menu');
        const hasDuplicateGroup = await this.user.hasGroup('mh_all_in_one_hide_action_menu.group_hide_duplicate_menu');
        const hasExportGroup = await this.user.hasGroup('mh_all_in_one_hide_action_menu.group_hide_export_menu');
        const hideArchiveGroup = await this.user.hasGroup('mh_all_in_one_hide_action_menu.group_hide_archive_menu');
        const hideUnarchiveGroup = await this.user.hasGroup('mh_all_in_one_hide_action_menu.group_hide_unarchive_menu');

        const hasExportAllGroup = await this.user.hasGroup('mh_all_in_one_hide_action_menu.group_hide_export_all_button');

        if (hasDeleteGroup || hasDuplicateGroup || hasExportGroup || hideArchiveGroup || hideUnarchiveGroup || hasExportAllGroup) {
            const currentModel = this.props.resModel;
            // console.log('Current model:', currentModel);

            const configModel = await this.orm.searchRead(
                "hide.action.menu.button.config",
                [["model_id.model", "=", currentModel]],
                ["is_active"]
            );

            if (configModel.length > 0) {
                if (hasDeleteGroup) {
                    this.state.hideDeleteListMenu = configModel[0].is_active;
                }
                if (hasDuplicateGroup) {
                    this.state.hideDuplicateListMenu = configModel[0].is_active;
                }
                if (hasExportGroup) {
                    this.state.hideExportListMenu = configModel[0].is_active;
                }
                if (hideArchiveGroup) {
                    this.state.hideArchiveListMenu = configModel[0].is_active;
                }
                if (hideUnarchiveGroup) {
                    this.state.hideUnarchiveListMenu = configModel[0].is_active;
                }
                if (hasExportAllGroup) {
                    this.state.hideExportAllListButton = configModel[0].is_active;
                }
            }
        }
    } catch (error) {
        console.error('Error fetching config:', error);
    }
};

const originalGetStaticActionMenuItemsList = ListController.prototype.getStaticActionMenuItems;
ListController.prototype.getStaticActionMenuItems = function () {
    const menuItems = originalGetStaticActionMenuItemsList.call(this);
    if (this.state.hideDeleteListMenu && menuItems.hasOwnProperty('delete')) {
        delete menuItems.delete;
    }
    if (this.state.hideDuplicateListMenu && menuItems.hasOwnProperty('duplicate')) {
        delete menuItems.duplicate;
    }
    if (this.state.hideExportListMenu && menuItems.hasOwnProperty('export')) {
        delete menuItems.export;
    }
    if (this.state.hideArchiveListMenu && menuItems.hasOwnProperty('archive')) {
        delete menuItems.archive;
    }
    if (this.state.hideUnarchiveListMenu && menuItems.hasOwnProperty('unarchive')) {
        delete menuItems.unarchive;
    }
    return menuItems;
};

