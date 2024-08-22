/** @odoo-module */
import { FormController } from '@web/views/form/form_controller';
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { formView } from '@web/views/form/form_view';

export class CombinedHideActionsFormController extends FormController {
    async fetchConfig() {
        this.orm = useService("orm");
        this.user = useService("user");

        this.hideDeleteMenu = false;
        this.hideDuplicateMenu = false;
        this.hideExportMenu = false;
        this.hideArchiveMenu = false;
        this.hideUnarchiveMenu = false;

        // Check for user group permissions
        const hasDeleteGroup = await this.user.hasGroup('mh_all_in_one_hide_action_menu.group_hide_delete_menu');
        const hasDuplicateGroup = await this.user.hasGroup('mh_all_in_one_hide_action_menu.group_hide_duplicate_menu');
        const hasExportGroup = await this.user.hasGroup('mh_all_in_one_hide_action_menu.group_hide_export_menu');
        const hideArchiveGroup = await this.user.hasGroup('mh_all_in_one_hide_action_menu.group_hide_archive_menu');
        const hideUnarchiveGroup = await this.user.hasGroup('mh_all_in_one_hide_action_menu.group_hide_unarchive_menu');

        if (hasDeleteGroup || hasDuplicateGroup || hasExportGroup || hideArchiveGroup || hideUnarchiveGroup) {
            const currentModel = this.props.resModel;

            try {
                const configModel = await this.orm.searchRead(
                    "hide.action.menu.button.config",
                    [["model_id.model", "=", currentModel]],
                    ["is_active"]
                );

                if (configModel.length > 0) {
                    if (hasDeleteGroup) {
                        this.hideDeleteMenu = configModel[0].is_active;
                    }
                    if (hasDuplicateGroup) {
                        this.hideDuplicateMenu = configModel[0].is_active;
                    }
                    if (hasExportGroup) {
                        this.hideExportMenu = configModel[0].is_active;
                    }
                    if (hideArchiveGroup) {
                        this.hideArchiveMenu = configModel[0].is_active;
                    }
                    if (hideUnarchiveGroup) {
                        this.hideUnarchiveMenu = configModel[0].is_active;
                    }
                }
            } catch (error) {
                console.error('Error fetching configuration:', error);
            }
        }
    }

    async setup() {
        super.setup();
        await this.fetchConfig();
    }

    getActionMenuItems() {
        const menuItems = super.getActionMenuItems();

        // Hide Delete Action
        if (this.hideDeleteMenu) {
            const deleteActionIndex = menuItems.other.findIndex((item) => item.key === "delete");
            if (deleteActionIndex !== -1) {
                menuItems.other.splice(deleteActionIndex, 1);
            }
        }

        // Hide Duplicate Action
        if (this.hideDuplicateMenu) {
            const duplicateActionIndex = menuItems.other.findIndex((item) => item.key === "duplicate");
            if (duplicateActionIndex !== -1) {
                menuItems.other.splice(duplicateActionIndex, 1);
            }
        }

        // Hide Export Action
        if (this.hideExportMenu) {
            const exportActionIndex = menuItems.other.findIndex((item) => item.key === "export");
            if (exportActionIndex !== -1) {
                menuItems.other.splice(exportActionIndex, 1);
            }
        }

        // Hide Archive Action
        if (this.hideArchiveMenu) {
            const archiveActionIndex = menuItems.other.findIndex((item) => item.key === "archive");
            if (archiveActionIndex !== -1) {
                menuItems.other.splice(archiveActionIndex, 1);
            }
        }

        // Hide Unarchive Action
        if (this.hideUnarchiveMenu) {
            const unarchiveActionIndex = menuItems.other.findIndex((item) => item.key === "unarchive");
            if (unarchiveActionIndex !== -1) {
                menuItems.other.splice(unarchiveActionIndex, 1);
            }
        }

        return menuItems;
    }
}

// Extend the form view controller globally in the registry
const formViewConfig = registry.category("views").get("form");
formViewConfig.Controller = CombinedHideActionsFormController;
