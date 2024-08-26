/** @odoo-module */

import { FormController } from '@web/views/form/form_controller';
import { useService } from "@web/core/utils/hooks";
import { onMounted, useState } from "@odoo/owl";

const originalSetupForm = FormController.prototype.setup;
FormController.prototype.setup = function () {
    originalSetupForm.call(this);
    this.orm = useService("orm");
    this.user = useService("user");
    this.state = useState({
        hideDeleteFormMenu: false,
        hideDuplicateFormMenu: false,
        hideExportFormMenu: false,
        hideArchiveFormMenu: false,
        hideUnarchiveFormMenu: false,
    });

    // Fetch configuration on component mount
    onMounted(() => {
        this.fetchConfig();
    });
};

FormController.prototype.fetchConfig = async function () {
    // console.log('Fetching config...');
    try {
        // Check if the logged-in user has the specific group
        const hasDeleteGroup = await this.user.hasGroup('mh_all_in_one_hide_action_menu.group_hide_delete_menu');
        const hasDuplicateGroup = await this.user.hasGroup('mh_all_in_one_hide_action_menu.group_hide_duplicate_menu');
        const hasExportGroup = await this.user.hasGroup('mh_all_in_one_hide_action_menu.group_hide_export_menu');
        const hideArchiveGroup = await this.user.hasGroup('mh_all_in_one_hide_action_menu.group_hide_archive_menu');
        const hideUnarchiveGroup = await this.user.hasGroup('mh_all_in_one_hide_action_menu.group_hide_unarchive_menu');

        if (hasDeleteGroup || hasDuplicateGroup || hasExportGroup || hideArchiveGroup || hideUnarchiveGroup) {
            const currentModel = this.props.resModel;
            // console.log('Current model:', currentModel);

            const configModel = await this.orm.searchRead(
                "hide.action.menu.button.config",
                [["model_id.model", "=", currentModel]],
                ["is_active"]
            );

            if (configModel.length > 0) {
                if (hasDeleteGroup) {
                    this.state.hideDeleteFormMenu = configModel[0].is_active;
                }
                if (hasDuplicateGroup) {
                    this.state.hideDuplicateFormMenu = configModel[0].is_active;
                }
                if (hasExportGroup) {
                    this.state.hideExportFormMenu = configModel[0].is_active;
                }
                if (hideArchiveGroup) {
                    this.state.hideArchiveFormMenu = configModel[0].is_active;
                }
                if (hideUnarchiveGroup) {
                    this.state.hideUnarchiveFormMenu = configModel[0].is_active;
                }
            }
        }
    } catch (error) {
        console.error('Error fetching config:', error);
    }
};

const originalGetStaticActionMenuItemsForm = FormController.prototype.getStaticActionMenuItems;
FormController.prototype.getStaticActionMenuItems = function () {
    const menuItems = originalGetStaticActionMenuItemsForm.call(this);
    if (this.state.hideDeleteFormMenu && menuItems.hasOwnProperty('delete')) {
        delete menuItems.delete;
    }
    if (this.state.hideDuplicateFormMenu && menuItems.hasOwnProperty('duplicate')) {
        delete menuItems.duplicate;
    }
    if (this.state.hideExportFormMenu && menuItems.hasOwnProperty('export')) {
        delete menuItems.export;
    }
    if (this.state.hideArchiveFormMenu && menuItems.hasOwnProperty('archive')) {
        delete menuItems.archive;
    }
    if (this.state.hideUnarchiveFormMenu && menuItems.hasOwnProperty('unarchive')) {
        delete menuItems.unarchive;
    }
    return menuItems;
};

