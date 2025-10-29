/** @odoo-module **/

import { AccountReportFilters } from "@account_reports/components/account_report/filters/filters";
import { patch } from "@web/core/utils/patch";
const { DateTime } = luxon;
import { _t } from "@web/core/l10n/translation";
import { formatDate } from "@web/core/l10n/dates";

patch(AccountReportFilters.prototype, {
    //------------------------------------------------------------------
    // Lifecycle
    //------------------------------------------------------------------
    setup() {
        super.setup?.();
        if (!this.controller.options.check_date) {
            this.controller.options.check_date = {};
        }
    },

    //------------------------------------------------------------------
    // Toggle visibility
    //------------------------------------------------------------------
    async toggleCheckDateFilter() {
        this.controller.options.check_date_filter = !this.controller.options.check_date_filter;
        await this.controller.reload("check_date_filter", this.controller.options);
    },

    //------------------------------------------------------------------
    // Handle dropdown selections
    //------------------------------------------------------------------
    selectCheckDateFilter(filter) {
        if (!this.controller.options.check_date) {
            this.controller.options.check_date = {};
        }

        // Toggle off if same filter clicked again
        if (this.controller.options.check_date.filter === filter) {
            this.controller.options.check_date = {
                filter: null,
                date_from: null,
                date_to: null,
                string: _t("Check Date"),
            };
            this.render();
            this._reloadCheckDate();
            return;
        }

        const now = DateTime.now();
        let from = null;
        let to = null;

        switch (filter) {
            case "today":
                from = null;
                to = now.endOf("day");
                break;
                // from = to = now;
                // break;
            case "month":
                from = now.startOf("month");
                to = now.endOf("month");
                break;
            case "quarter":
                from = now.startOf("quarter");
                to = now.endOf("quarter");
                break;
            case "year":
                from = now.startOf("year");
                to = now.endOf("year");
                break;
            case "custom":
                // Just activate the custom filter and wait for user to pick dates
                this.controller.options.check_date.filter = "custom";
                this.controller.options.check_date.string = _t("Select Range");
                this.render();
                return;
            default:
                this.controller.options.check_date = {
                    filter: null,
                    date_from: null,
                    date_to: null,
                    string: _t("Check Date"),
                };
                this.render();
                return;
        }

        // Apply prebuilt filter values
        // this.controller.options.check_date.filter = filter;
        // this.controller.options.check_date.date_from = from.toISODate();
        // this.controller.options.check_date.date_to = to.toISODate();
        // this.controller.options.check_date.string = `${formatDate(from)} → ${formatDate(to)}`;
        // ✅ Apply selected filter values safely (handles nulls)
        this.controller.options.check_date.filter = filter;
        this.controller.options.check_date.date_from = from ? from.toISODate() : null;
        this.controller.options.check_date.date_to = to ? to.toISODate() : null;

        if (!from && to) {
            this.controller.options.check_date.string = `${_t("As of")} ${formatDate(to)}`;
        } else if (from && to) {
            this.controller.options.check_date.string = `${formatDate(from)} → ${formatDate(to)}`;
        } else {
            this.controller.options.check_date.string = _t("Check Date");
        }
        this._reloadCheckDate();
    },

    //------------------------------------------------------------------
    // Handle "From" and "To" date changes
    //------------------------------------------------------------------
    async setCheckDateFrom(dateFrom) {
        if (!this.controller.options.check_date)
            this.controller.options.check_date = {};

        this.controller.options.check_date.date_from = dateFrom || null;

        // If both from & to exist, reload immediately
        if (this.controller.options.check_date.date_from && this.controller.options.check_date.date_to) {
            await this._reloadCheckDate();
        } else {
            this.render();
        }
    },

    async setCheckDateTo(dateTo) {
        if (!this.controller.options.check_date)
            this.controller.options.check_date = {};

        this.controller.options.check_date.date_to = dateTo || null;

        // If both from & to exist, reload immediately
        if (this.controller.options.check_date.date_from && this.controller.options.check_date.date_to) {
            await this._reloadCheckDate();
        } else {
            this.render();
        }
    },

    //------------------------------------------------------------------
    // Helper to update displayed date label
    //------------------------------------------------------------------
    async _reloadCheckDate() {
        const opts = this.controller.options;
        let dateFrom = opts.check_date?.date_from;
        let dateTo = opts.check_date?.date_to;

        if (typeof dateFrom === "string") dateFrom = DateTime.fromISO(dateFrom);
        if (typeof dateTo === "string") dateTo = DateTime.fromISO(dateTo);

        if (dateFrom && dateTo) {
            opts.check_date.string = `${formatDate(dateFrom)} → ${formatDate(dateTo)}`;
        } else if (dateFrom) {
            opts.check_date.string = `${formatDate(dateFrom)} →`;
        } else if (dateTo) {
            opts.check_date.string = `→ ${formatDate(dateTo)}`;
        } else {
            opts.check_date.string = _t("Check Date");
        }

        await this.controller.reload("check_date", opts);
    },

    //------------------------------------------------------------------
    // Template data helpers
    //------------------------------------------------------------------
    dateFrom(field) {
        if (field === "check_date" && this.controller.options.check_date) {
            const val = this.controller.options.check_date.date_from;
            return val ? DateTime.fromISO(val) : null;
        }
        return null;
    },

    dateTo(field) {
        if (field === "check_date" && this.controller.options.check_date) {
            const val = this.controller.options.check_date.date_to;
            return val ? DateTime.fromISO(val) : null;
        }
        return null;
    },
});







// /** @odoo-module **/
//
// import { AccountReportFilters } from "@account_reports/components/account_report/filters/filters";
// import { patch } from "@web/core/utils/patch";
// const { DateTime } = luxon;
//
// patch(AccountReportFilters.prototype, {
//     /**
//      * Toggle Check Date filter visibility
//      */
//     async toggleCheckDateFilter() {
//         this.controller.options.check_date_filter = !this.controller.options.check_date_filter;
//         await this.controller.reload("check_date_filter", this.controller.options);
//     },
//
//     /**
//      * Set "Check Date From" value
//      */
//     async setCheckDateFrom(dateFrom) {
//         if (!this.controller.options.check_date) {
//             this.controller.options.check_date = {};
//         }
//
//         // Ensure Luxon DateTime consistency
//         this.controller.options.check_date.date_from =
//             dateFrom instanceof DateTime ? dateFrom : DateTime.fromISO(dateFrom);
//
//         await this._reloadCheckDate();
//     },
//
//     /**
//      * Set "Check Date To" value
//      */
//     async setCheckDateTo(dateTo) {
//         if (!this.controller.options.check_date) {
//             this.controller.options.check_date = {};
//         }
//
//         // Ensure Luxon DateTime consistency
//         this.controller.options.check_date.date_to =
//             dateTo instanceof DateTime ? dateTo : DateTime.fromISO(dateTo);
//
//         await this._reloadCheckDate();
//     },
//
//     /**
//      * Helper: reload report when check date changes
//      */
//     async _reloadCheckDate() {
//         const opts = { ...this.controller.options };
//
//         // Ensure all date fields are Luxon DateTime before reload
//         if (opts.date?.date_from && typeof opts.date.date_from === "string") {
//             opts.date.date_from = DateTime.fromISO(opts.date.date_from);
//         }
//         if (opts.date?.date_to && typeof opts.date.date_to === "string") {
//             opts.date.date_to = DateTime.fromISO(opts.date.date_to);
//         }
//         if (opts.check_date?.date_from && typeof opts.check_date.date_from === "string") {
//             opts.check_date.date_from = DateTime.fromISO(opts.check_date.date_from);
//         }
//         if (opts.check_date?.date_to && typeof opts.check_date.date_to === "string") {
//             opts.check_date.date_to = DateTime.fromISO(opts.check_date.date_to);
//         }
//
//         await this.controller.reload("check_date", opts);
//     },
//
//     /**
//      * Helper: get "from" value for template binding
//      */
//     dateFrom(field) {
//         const dateObj =
//             field === "check_date"
//                 ? this.controller.options.check_date
//                 : this.controller.options.date;
//
//         if (!dateObj?.date_from) return null;
//         return dateObj.date_from instanceof DateTime
//             ? dateObj.date_from
//             : DateTime.fromISO(dateObj.date_from);
//     },
//
//     /**
//      * Helper: get "to" value for template binding
//      */
//     dateTo(field) {
//         const dateObj =
//             field === "check_date"
//                 ? this.controller.options.check_date
//                 : this.controller.options.date;
//
//         if (!dateObj?.date_to) return null;
//         return dateObj.date_to instanceof DateTime
//             ? dateObj.date_to
//             : DateTime.fromISO(dateObj.date_to);
//     },
// });


