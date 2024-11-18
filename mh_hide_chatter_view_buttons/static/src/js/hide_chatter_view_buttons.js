/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { registry } from "@web/core/registry";
import { Chatter } from "@mail/core/web/chatter";
import {onMounted, onWillStart, useState} from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";


export class ChatterHide extends Chatter {
    static template = "mh_hide_chatter_view_buttons.Chatter";
}


// Define the patch
patch(Chatter.prototype, {
    setup() {
        // Call the original setup method if it exists
        super.setup();
        this.orm = useService("orm");
        this.user = useService("user");
        this.state = useState({
            hideSendMessage: false,
            hideLogNote: false,
            hideActivities: false,
            hideFileUpload: false,
            hideMailFollowers: false,
            hideFollow: false,
        });
        // Fetch configuration on component mount
        // onMounted(() => {
        //     this.fetchConfig();
        // });
        this.fetchConfig();
    },

    async fetchConfig() {
        const uid = this.user.userId;
        const currentModel = this.props.threadModel;
        const chatter = await this.orm.searchRead(
            "hide.chatter.view.buttons",
            [["user_id.id", "=", uid],["is_active", "=", true]],
            ["hide_chatter_line_ids"]
        );

        if (chatter.length > 0) {
            const chatterId = chatter[0].id;
            const chatterLines = await this.orm.searchRead(
                "hide.chatter.view.buttons.lines",
                [["hide_chatter_id", "=", chatterId],["model_id", "=", currentModel]],
                ["model_id", "hide_send_message","hide_log_note","hide_activities","hide_file_upload","hide_mail_followers","hide_follow"]
            );
            if (chatterLines.length > 0) {
                this.state.hideSendMessage = chatterLines[0].hide_send_message;
                this.state.hideLogNote = chatterLines[0].hide_log_note;
                this.state.hideActivities = chatterLines[0].hide_activities;
                this.state.hideFileUpload = chatterLines[0].hide_file_upload;
                this.state.hideMailFollowers = chatterLines[0].hide_mail_followers;
                this.state.hideFollow = chatterLines[0].hide_follow;
            }
        }
    },
});




