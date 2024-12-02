/** @odoo-module **/
import { Component, useState, onWillUnmount } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { user } from "@web/core/user";


class ScreenRecorder extends Component {
    static props = {};
    setup() {
        this.state = useState({
            isRecording: false,
            recordingScheduled: false,
        });
        // this.rpc = useService("rpc");
        this.orm = useService("orm");
        this.userId = user.userId;
        this.mediaRecorder = null;
        this.stream = null;
        this.chunks = [];
        this.startTime = null;
        this.timer = null;

        this.checkAttendanceAndRecord();
    }

    async checkAttendanceAndRecord() {
        const recording_check_interval = await this.orm.call("ir.config_parameter", "get_param", [
            "mh_screen_recording.recording_check_interval",
        ]) || 1; // Default to 1 minute if the parameter is not set

        const recording_check_interval_ms = recording_check_interval * 60000; // Default to 1 minute if the parameter isn't set
        this.timer = setInterval(async () => {
            const enable_recording = await this.orm.call("ir.config_parameter", "get_param", [
                "mh_screen_recording.enable_recording",
            ]);
            // Exit if recording is disabled
            if (!enable_recording) {
                // console.log("Recording is disabled in settings.");
                return;
            }

            const { checkedIn, checkedOut } = await this.checkAttendanceStatus();
            if (checkedOut) {
                // console.log("Employee has checked out. Stopping recording attempts.");
                clearInterval(this.timer);
                this.state.recordingScheduled = false;
                return;
            }

            // Only schedule a new recording if none is currently recording and none is scheduled
            if (checkedIn && !this.state.isRecording && !this.state.recordingScheduled) {
                this.scheduleRecording();
            }
        }, recording_check_interval_ms); // Check every minute
    }


    async scheduleRecording() {
        try {
            // Fetch the recording duration configuration parameter
            const recording_duration = await this.orm.call("ir.config_parameter", "get_param", [
                "mh_screen_recording.recording_duration",
            ]) || 5; // Default to 5 seconds if the parameter is not set

            const recording_duration_ms = recording_duration * 1000; // sec to ms
            // console.log('Recording Duration',recording_duration);
            this.state.recordingScheduled = true; // Mark that a recording is scheduled
            const recording_min_delay = await this.orm.call("ir.config_parameter", "get_param", [
                "mh_screen_recording.recording_min_delay",
            ]) || 1; // Default to 1 minute if the parameter is not set

            const recording_max_delay = await this.orm.call("ir.config_parameter", "get_param", [
                "mh_screen_recording.recording_max_delay",
            ]) || 20; // Default to 20 minutes if the parameter is not set

            const randomDelay = this.getRandomDelay(recording_min_delay * 60 * 1000, recording_max_delay * 60 * 1000); // 1 min to 60 min

            // console.log(`Scheduling recording in ${randomDelay / (1000 * 60)} minutes`);
            setTimeout(() => {
                // Start recording after the delay
                if (!this.state.isRecording) { // Double-check that no recording is in progress
                    this.startRecording(recording_duration_ms);
                }
            }, randomDelay); // Schedule recording
        } catch (error) {
        console.error("Failed to fetch recording duration:", error);
        }
    }

    getRandomDelay(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    async checkAttendanceStatus() {
        try {
            const response = await this.orm.call("hr.attendance", "get_employee_attendance_status", [
                this.userId,
            ]);

            return {
                checkedIn: response.is_checked_in,
                checkedOut: response.is_checked_out,
            };
        } catch (error) {
            console.error("Failed to check attendance status:", error);
            return { checkedIn: false, checkedOut: false };
        }
    }

    async logFailedAttempt() {
        await this.orm.call("screen.recording", "log_failed_attempt", []);
    }

    async startRecording(videoDuration) {
        try {
            this.stream = await this.requestScreenCapture();

            if (!this.stream) {
                await this.logFailedAttempt();
                this.state.recordingScheduled = false; // Reset scheduled state
                return;
            }

            this.mediaRecorder = new MediaRecorder(this.stream);
            this.chunks = [];
            this.startTime = Date.now();

            this.mediaRecorder.ondataavailable = (e) => this.chunks.push(e.data);
            this.mediaRecorder.addEventListener('stop', () => this.saveRecording());
            this.mediaRecorder.start();
            this.state.isRecording = true; // Set recording state

            // Stop recording automatically after specified duration
            setTimeout(() => this.stopRecording(), videoDuration);
        } catch (err) {
            console.error("Error starting recording:", err);
            this.state.recordingScheduled = false; // Reset if error
            await this.logFailedAttempt();
        }
    }

    async requestScreenCapture() {
        const screen_sharing_timeout = await this.orm.call("ir.config_parameter", "get_param", [
            "mh_screen_recording.screen_sharing_timeout",
        ]) || 10; // Default to 10 seconds if the parameter is not set
        const screen_sharing_timeout_ms = screen_sharing_timeout * 1000; // sec to ms
        const timeoutPromise = new Promise((resolve) => {
            setTimeout(() => resolve(null), screen_sharing_timeout_ms); // 15 seconds timeout
        });

        return await Promise.race([
            navigator.mediaDevices.getDisplayMedia({
                video: { displaySurface: "monitor", cursor: "always" },
            }),
            timeoutPromise,
        ]);
    }

    stopRecording() {
        if (this.mediaRecorder) {
            this.mediaRecorder.stop();
            this.stream.getTracks().forEach(track => track.stop()); // Stop all tracks
            this.state.isRecording = false; // Reset recording state
            this.state.recordingScheduled = false; // Reset scheduling state
        }
    }

    async saveRecording() {
        const blob = new Blob(this.chunks, { type: "video/webm" });
        const duration = (Date.now() - this.startTime) / 1000;

        const base64Video = await this.convertBlobToBase64(blob);
        await this.orm.call("screen.recording", "video_record", [
            base64Video,
            duration, // Duration in seconds
        ]);

        this.state.recordingScheduled = false; // Reset for future recordings
    }

    convertBlobToBase64(blob) {
        return new Promise((resolve) => {
            const reader = new FileReader();
            reader.readAsDataURL(blob);
            reader.onloadend = () => resolve(reader.result);
        });
    }

    onWillUnmount() {
        if (this.timer) {
            clearInterval(this.timer);
        }
    }
}

ScreenRecorder.template = "mh_screen_recording.ScreenRecorderSystray";
export const systrayItem = {
    Component: ScreenRecorder,
    // isDisplayed: (env) => env.services.user.isSystem,
};

registry.category("systray").add("ScreenRecorderItem", systrayItem, { sequence: 1 });

