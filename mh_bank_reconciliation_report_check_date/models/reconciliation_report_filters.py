from datetime import date
import logging
from odoo import models, fields, _
from odoo.exceptions import UserError
from odoo.tools import SQL

_logger = logging.getLogger(__name__)


class AccountReport(models.Model):
    _inherit = "account.report"

    # Boolean to enable the filter
    filter_check_date = fields.Boolean(
        string="Check Date Filter",
        compute=lambda self: self._compute_report_option_filter('filter_check_date'),
        readonly=False,
        store=True,
        depends=['root_report_id', 'section_main_report_ids']
    )

    def _init_options_check_date(self, options, previous_options=None):
        """
        Initialize the check_date filter in report options.
        Called automatically when building options.
        """
        if not self.filter_check_date:
            return

        options['filter_check_date'] = True
        # use key 'check_date'
        options['check_date'] = previous_options.get('check_date', {
            'date_from': False,
            'date_to': False,
        })
        # Optionally, set defaults:
        # if not options['check_date']['date_from']:
        #     options['check_date']['date_from'] = fields.Date.today().replace(day=1)
        # if not options['check_date']['date_to']:
        #     options['check_date']['date_to'] = fields.Date.today()

    def _get_options_check_date_domain(self, options):
        """Return domain for the check_date filter on payment’s check_date."""
        domain = []
        cd = options.get('check_date')
        if cd:
            dfrom = cd.get('date_from')
            dto = cd.get('date_to')
            if dfrom:
                domain.append(("payment_id.check_date", ">=", dfrom))
            if dto:
                domain.append(("payment_id.check_date", "<=", dto))
        return domain

    def _get_options_domain(self, options, date_scope):
        """
        Extend base domain to include check_date filter domain.
        """
        domain = super()._get_options_domain(options, date_scope)
        # append our filter domain
        domain += self._get_options_check_date_domain(options)
        return domain


class AccountBankReconciliationReportHandler(models.AbstractModel):
    _inherit = "account.bank.reconciliation.report.handler"

    def _get_custom_display_config(self):
        return {
            'templates': {
                'AccountReportFilters': 'mh_bank_reconciliation_report_check_date.BRFilter',
            },
        }

    def _custom_options_initializer(self, report, options, previous_options):
        super()._custom_options_initializer(report, options, previous_options=previous_options)
        options['check_date_filter'] = previous_options.get('check_date_filter', False)

        if options.get('check_date_filter'):
            self._apply_check_date_filter(options)

    def _apply_check_date_filter(self, options):
        """Filter lines based on check_date range."""
        forced_domain = options.setdefault('forced_domain', [])
        forced_domain += [
            ('check_date', '>=', options['date']['date_from']),
            ('check_date', '<=', options['date']['date_to']),
        ]
