/** @odoo-module **/
import { registry } from '@web/core/registry';
import { CharField } from '@web/views/fields/char/char_field';
import { useRef, onMounted, onWillUpdateProps } from "@odoo/owl";

class VideoWidget extends CharField {
    setup() {
        super.setup();
        this.videoRef = useRef("videoElement");  // Create a reference for the video element
        onMounted(() => {
            this.updateVideoSrc();
        });

        onWillUpdateProps((nextProps) => {
            if (this.props.value !== nextProps.value) {
                this.videoRef.el.src = nextProps.value;
            }
        });

    }

    updateVideoSrc() {
        // Ensure the video element exists before setting the src attribute
        if (this.videoRef.el) {
            this.videoRef.el.src = this.props.value || '';  // Set src to the field's value or empty if undefined
        }else {
            this.videoRef.el.src = '';
        }
    }

}

VideoWidget.template = 'mh_screen_recording.VideoWidget';  // Template should contain a <video> element with `t-ref="videoElement"`

// Register the widget in the field registry
registry.category('fields').add('video_preview_widget', VideoWidget);



