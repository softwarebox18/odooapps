/** @odoo-module */
import { FormController } from '@web/views/form/form_controller';
import { useService } from "@web/core/utils/hooks";
const { onWillStart } = owl;

export class HideDuplicateMenuFormController extends FormController {
    async fetchConfig() {
        this.orm = useService("orm");
        this.user = useService("user");

        const hasGroup = await this.user.hasGroup('mh_hide_duplicate_menu_with_js_class.group_hide_duplicate_menu');
        if (hasGroup) {
            const currentModel = this.props.resModel;
            console.log('Current Model:', currentModel);

            try {
                const configModel = await this.orm.searchRead(
                    "hide.duplicate.button.config",
                    [["model_id.model", "=", currentModel]],
                    ["is_active"]
                );
                if (configModel.length > 0) {
                    const isActive = configModel[0].is_active;
                    this.hideDuplicateMenu = isActive;
                } else {
                    this.hideDuplicateMenu = false;
                }
            } catch (error) {
                console.error('Error fetching configuration:', error);
                this.hideDuplicateMenu = false;
            }
        } else {
            this.hideDuplicateMenu = false;
        }
    }

    async setup() {
        super.setup();
        this.hideDuplicateMenu = false;
        await this.fetchConfig();
    }

    getActionMenuItems() {
        const menuItems = super.getActionMenuItems();
        // console.log('Hide Duplicate Menu:', this.hideDuplicateMenu);
        if (this.hideDuplicateMenu) {
            // const duplicateActionIndex = menuItems.other.find((item) => item.key === "duplicate");
            const duplicateActionIndex = menuItems.other.findIndex((item) => item.key === "duplicate");
            if (duplicateActionIndex !== -1) {
                // console.log('Removing Duplicate Action:', menuItems.other[duplicateActionIndex]);
                menuItems.other.splice(duplicateActionIndex, 1);
                // console.log('Updated Menu Items:', menuItems.other);
            }
        }
        return menuItems;
    }
}

