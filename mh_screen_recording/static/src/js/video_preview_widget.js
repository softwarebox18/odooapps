/** @odoo-module **/
import { registry } from '@web/core/registry';
import { CharField } from '@web/views/fields/char/char_field';
import {useRef, onMounted, onWillUpdateProps, useState} from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";

export class VideoWidget extends CharField {
    static template = "mh_screen_recording.VideoWidget";

    setup() {
        super.setup();
        this.videoRef = useRef("videoElement");  // Create a reference for the video element
        onMounted(() => {
            this.updateVideoSrc();
        });
        onWillUpdateProps((nextProps) => {
            if (this.props.record.data.video_url !== nextProps.record.data.video_url) {
                this.videoRef.el.src = nextProps.record.data.video_url;
            }
        });
    }

    updateVideoSrc() {
        // Ensure the video element exists before setting the src attribute
        if (this.videoRef.el) {
            this.videoRef.el.src = this.props.record.data.video_url || '';  // Set src to the field's value or empty if undefined
        }else {
            this.videoRef.el.src = '';
        }
    }

    get value() {
        return this.props.record.data[this.props.name];
    }
}

// Register the component
export const videoWidget = {
    component: VideoWidget,
    displayName: _t("Video Widget"),
    supportedTypes: ["char"],
    isEmpty: (record, fieldName) => record.data[fieldName] === false,
};

registry.category("fields").add("video_preview_widget", videoWidget);




