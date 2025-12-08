/** @odoo-module */

import { AccountReportFilters } from "@account_reports/components/account_report/filters/filters";
import { patch } from "@web/core/utils/patch";
console.log('1111111111111');

patch(AccountReportFilters.prototype, {
    //------------------------------------------------------------------
    setup() {
        super.setup?.();

        // Ensure currencies array exists
        this.controller.options.currencies = this.controller.options.currencies || [];

        // If no selected currency, default to All (id: false)
        if (this.controller.options.currencies_selected === undefined) {
            this.controller.options.currencies_selected = false;
            this.controller.options.currencies_selected_name = 'All';
        }

        this._markSelectedCurrency();
    },

    //------------------------------------------------------------------
    // Handle dropdown selection
    //------------------------------------------------------------------
    async filterCurrency(currency) {
        // Save selected currency in options
        if (currency.id === false) {
            this.controller.options.currencies_selected = false;
            this.controller.options.currencies_selected_name = 'All';
        } else {
            this.controller.options.currencies_selected = currency.id;
            this.controller.options.currencies_selected_name = currency.name;
        }

        // Reload report
        await this.controller.reload('currencies', this.controller.options);

        // Re-mark selected currency after reload
        this._markSelectedCurrency();
    },

    //------------------------------------------------------------------
    // Helper to mark selected currency
    //------------------------------------------------------------------
    _markSelectedCurrency() {
        const selectedId = this.controller.options.currencies_selected;
        this.controller.options.currencies.forEach(c => {
            c.selected = selectedId !== false && c.id === selectedId;
        });
    },
});


// patch(AccountReportFilters.prototype, {
//     //------------------------------------------------------------------
//     // Lifecycle
//     //------------------------------------------------------------------
//     setup() {
//         super.setup?.();
//         if (!this.controller.options.currencies) {
//             this.controller.options.currencies = [];
//         }
//         if (!this.controller.options.currencies_selected) {
//             this.controller.options.currencies_selected = this.controller.options.currencies_selected || this.env.company.currency_id;
//         }
//         if (!this.controller.options.currencies_selected_name) {
//             this.controller.options.currencies_selected_name = this.controller.options.currencies_selected_name || this.env.company.currency_id.name;
//         }
//
//         // Mark selected currency
//         const selectedId = this.controller.options.currencies_selected;
//         this.controller.options.currencies.forEach(c => {
//             c.selected = c.id === selectedId;
//         });
//         console.log('22222222222',this.controller.options.currencies);
//     },
//
//     //------------------------------------------------------------------
//     // Handle dropdown selection
//     //------------------------------------------------------------------
//     async filterCurrency(currency) {
//         if (!this.controller.options.currencies) {
//             this.controller.options.currencies = [];
//         }
//
//         // Toggle selected
//         this.controller.options.currencies.forEach(c => c.selected = false);
//         currency.selected = true;
//
//         // Save in options
//         this.controller.options.currencies_selected = currency.id;
//         this.controller.options.currencies_selected_name = currency.name;
//
//         // Reload the report
//         await this.controller.reload("currencies", this.controller.options);
//     },
// });


// patch(AccountReportFilters.prototype,{
//
//     //Extend base class and add new method for currency
//     async filterCurrency(currency) {
//         console.log('2222222222222222');
//         currency.selected = !currency.selected;
//         if (currency.selected){
//             this.controller.options.currencies_selected = parseInt(currency.id)
//             this.controller.options.currencies_selected_name = currency.name
//         }
//         console.log(currency)
//         await this.controller.reload('currencies', this.controller.options);
//     }
//
// });