/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { ChatterTopbar } from '@mail/components/chatter_topbar/chatter_topbar';
const { useState, onMounted } = owl.hooks;
import { useService } from "@web/core/utils/hooks";

// Define the patch
patch(ChatterTopbar.prototype, "mh_hide_chatter_view_buttons.hide_chatter_view_patch", {
    setup() {
        // Call the original setup method if it exists
        this._super(...arguments);
        this.rpc = useService("rpc");
        this.user = this.env.session.uid;
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
        const currentModel = this.chatter.threadModel;
        const chatter = await this.rpc({
            model: 'hide.chatter.view.buttons',
            method: 'search_read',
            domain: [["user_id.id", "=", this.user],["is_active", "=", true]],
            fields: ['hide_chatter_line_ids'],
        });

        if (chatter.length > 0) {
            const chatterId = chatter[0].id;
            const chatterLines = await this.rpc({
                model: 'hide.chatter.view.buttons.lines',
                method: 'search_read',
                domain: [["hide_chatter_id", "=", chatterId],["model", "=", currentModel]],
                fields: ["model_id", "hide_send_message","hide_log_note","hide_activities","hide_file_upload","hide_mail_followers","hide_follow"],
            });
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




