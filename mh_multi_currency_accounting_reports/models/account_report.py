
from odoo import models, _,api, fields
from odoo.exceptions import AccessError
from odoo.tools.misc import formatLang
from odoo.tools.misc import format_date, formatLang
import logging
_logger = logging.getLogger(__name__)
import datetime
from odoo.tools import SQL
from odoo.tools.misc import format_date
from dateutil.relativedelta import relativedelta
from itertools import chain


NUMBER_FIGURE_TYPES = ('float', 'integer', 'monetary', 'percentage')

class AccountReport(models.Model):
    _inherit = 'account.report'

    def _build_column_dict(
            self, col_value, col_data,
            options=None, currency=False, digits=1,
            column_expression=None, has_sublines=False,
            report_line_id=None,
    ):
        import datetime

        # print('222222222222222', self.name)
        # if not aged receivable/payable → use default Odoo logic
        if self.name not in (
                'Aged Receivable',
                'Aged Payable'
        ):
            return super()._build_column_dict(
                col_value, col_data, options, currency, digits,
                column_expression, has_sublines, report_line_id
            )

        # --------- CUSTOM LOGIC ONLY FOR AGED RECEIVABLE/PAYABLE ---------
        if col_value is None and col_data is None:
            return {}

        col_data = col_data or {}
        column_expression = column_expression or self.env['account.report.expression']
        options = options or {}

        blank_if_zero = column_expression.blank_if_zero or col_data.get('blank_if_zero', False)
        figure_type = column_expression.figure_type or col_data.get('figure_type', 'string')

        expr = col_data.get('expression_label')
        is_amount_currency_col = (expr == 'amount_currency')

        # Determine currency for formatting
        if is_amount_currency_col:
            # Keep original currency for Amount Currency column
            final_currency = currency or self.env.company.currency_id
        else:
            # Use report filter currency for other columns
            currency_data = options.get("currencies_selected")
            to_currency = self._extract_currency(currency_data)
            if not to_currency:
                to_currency = self.env['res.currency'].search(
                    [('name', '=', options.get('currencies_selected_name'))], limit=1)
            final_currency = to_currency or currency or self.env.company.currency_id
            # Convert value
            if isinstance(col_value, (int, float)):
                # Use company's currency for conversion base
                company_currency = self.env.company.currency_id
                col_value = company_currency._convert(col_value, final_currency,
                                                      date=datetime.datetime.strptime(options['date']['date_to'],
                                                                                      '%Y-%m-%d').date())

        # Format params
        format_params = {}
        if figure_type == 'monetary':
            format_params['currency_id'] = final_currency.id
        elif figure_type in ('float', 'percentage'):
            format_params['digits'] = digits

        return {
            'auditable': col_value is not None and column_expression.auditable,
            'blank_if_zero': blank_if_zero,
            'column_group_key': col_data.get('column_group_key'),
            'currency': final_currency,
            'currency_symbol': final_currency.symbol if options.get('multi_currency') else None,
            'digits': digits,
            'expression_label': expr,
            'figure_type': figure_type,
            'green_on_positive': column_expression.green_on_positive,
            'has_sublines': has_sublines,
            'is_zero': col_value is None or (
                    isinstance(col_value, (int, float))
                    and figure_type in NUMBER_FIGURE_TYPES
                    and self._is_value_zero(col_value, figure_type, format_params)
            ),
            'name': self._format_value(
                options, col_value, figure_type,
                format_params=format_params,
                blank_if_zero=blank_if_zero,
            ),
            'no_format': col_value,
            'report_line_id': report_line_id,
            'sortable': col_data.get('sortable', False),
        }

    # def _build_column_dict(
    #         self, col_value, col_data,
    #         options=None, currency=False, digits=1,
    #         column_expression=None, has_sublines=False,
    #         report_line_id=None,
    # ):
    #     import datetime
    #
    #     print('222222222222222', self.name)
    #     # if not aged receivable/payable → use default Odoo logic
    #     if self.name not in (
    #             'Aged Receivable',
    #             'Aged Payable'
    #     ):
    #         return super()._build_column_dict(
    #             col_value, col_data, options, currency, digits,
    #             column_expression, has_sublines, report_line_id
    #         )
    #
    #     # --------- CUSTOM LOGIC ONLY FOR AGED RECEIVABLE/PAYABLE ---------
    #     if col_value is None and col_data is None:
    #         return {}
    #
    #     col_data = col_data or {}
    #     column_expression = column_expression or self.env['account.report.expression']
    #     options = options or {}
    #
    #     blank_if_zero = column_expression.blank_if_zero or col_data.get('blank_if_zero', False)
    #     figure_type = column_expression.figure_type or col_data.get('figure_type', 'string')
    #
    #     expr = col_data.get('expression_label')
    #     is_amount_currency_col = (expr == 'amount_currency')
    #
    #     company_currency = self.env.company.currency_id
    #
    #     # Get selected currency
    #     currency_data = options.get("currencies_selected")
    #     to_currency = self._extract_currency(currency_data)
    #
    #     if not to_currency:
    #         to_currency = self.env['res.currency'].search(
    #             [('name', '=', options.get('currencies_selected_name'))], limit=1)
    #
    #     final_currency = to_currency or currency or company_currency
    #
    #     # Convert only numeric values for aged reports, except amount_currency column
    #     if (
    #             final_currency.id != company_currency.id
    #             and isinstance(col_value, (int, float))
    #             and not is_amount_currency_col  # <--- skip conversion for amount_currency
    #     ):
    #         col_value = company_currency._convert(
    #             col_value,
    #             final_currency,
    #             self.env.company,
    #             date=datetime.datetime.strptime(options['date']['date_to'], '%Y-%m-%d').date()
    #         )
    #
    #     # Format params
    #     format_params = {}
    #     if figure_type == 'monetary':
    #         format_params['currency_id'] = final_currency.id
    #     elif figure_type in ('float', 'percentage'):
    #         format_params['digits'] = digits
    #
    #     return {
    #         'auditable': col_value is not None and column_expression.auditable,
    #         'blank_if_zero': blank_if_zero,
    #         'column_group_key': col_data.get('column_group_key'),
    #         'currency': final_currency,
    #         'currency_symbol': final_currency.symbol if options.get('multi_currency') else None,
    #         'digits': digits,
    #         'expression_label': expr,
    #         'figure_type': figure_type,
    #         'green_on_positive': column_expression.green_on_positive,
    #         'has_sublines': has_sublines,
    #         'is_zero': col_value is None or (
    #                 isinstance(col_value, (int, float))
    #                 and figure_type in NUMBER_FIGURE_TYPES
    #                 and self._is_value_zero(col_value, figure_type, format_params)
    #         ),
    #         'name': self._format_value(
    #             options, col_value, figure_type,
    #             format_params=format_params,
    #             blank_if_zero=blank_if_zero,
    #         ),
    #         'no_format': col_value,
    #         'report_line_id': report_line_id,
    #         'sortable': col_data.get('sortable', False),
    #     }


    filter_multi_currencies = fields.Boolean(
        string="Multi Currencies Filter",
        compute=lambda self: self._compute_report_option_filter('filter_multi_currencies'),
        readonly=False,
        store=True,
        depends=['root_report_id', 'section_main_report_ids']
    )

    def _format_value(self, options, value, figure_type, format_params=None, blank_if_zero=False):
        """Formats a value for display in a report (not especially numerical).
        figure_type provides the type of formatting we want.
        """
        if value is None:
            return ''

        if figure_type == 'none':
            return value

        if isinstance(value, str) or figure_type == 'string':
            return str(value)

        if format_params is None:
            format_params = {}

        formatLang_params = {
            'rounding_method': 'HALF-UP',
            'rounding_unit': options.get('rounding_unit'),
        }

        # --- handle monetary values ---
        if figure_type == 'monetary':
            # currency: from format_params or fallback to company
            currency = self.env['res.currency'].browse(
                format_params['currency_id']) if 'currency_id' in format_params else self.env.company.currency_id
            if options.get('multi_currency'):
                formatLang_params['currency_obj'] = currency
            else:
                formatLang_params['digits'] = currency.decimal_places

        # --- integers ---
        elif figure_type == 'integer':
            formatLang_params['digits'] = 0

        # --- boolean ---
        elif figure_type == 'boolean':
            return _("Yes") if bool(value) else _("No")

        # --- date/datetime ---
        elif figure_type in ('date', 'datetime'):
            return format_date(self.env, value)

        # --- others: float, percentage, etc ---
        else:
            formatLang_params['digits'] = format_params.get('digits', 1)

        # --- check zero values ---
        if self._is_value_zero(value, figure_type, format_params):
            if blank_if_zero:
                return ''
            # make sure -0.0 becomes 0.0
            value = abs(value)

        if self._context.get('no_format'):
            return value

        # --- final formatting ---
        formatted_amount = formatLang(self.env, value, **formatLang_params)

        if figure_type == 'percentage':
            return f"{formatted_amount}%"

        return formatted_amount


    def _extract_currency(self, currency_data):
        """Accepts: int id OR dict {'id': x, 'name': y}
           Returns: currency record OR False
        """
        if not currency_data:
            return False

        # case 1: already an int ID
        if isinstance(currency_data, int):
            return self.env['res.currency'].browse(currency_data)

        # case 2: dict {'id':.., 'name':..}
        if isinstance(currency_data, dict):
            cid = currency_data.get('id')
            return self.env['res.currency'].browse(cid) if cid else False

        return False


    #Override base method
    def _init_options_currencies(self, options, previous_options=None):
        """ Initialize currencies for the report filter """
        if not self.filter_multi_currencies:
            return

        options['filter_multi_currencies'] = True

        options['currencies'] = []
        selected_currency_id = self.env.company.currency_id.id
        selected_currency_name = self.env.company.currency_id.name

        if previous_options:
            selected_currency_id = previous_options.get('currencies_selected', selected_currency_id)
            selected_currency_name = previous_options.get('currencies_selected_name', selected_currency_name)

        for currency in self.env['res.currency'].search([]):
            options['currencies'].append({
                'id': currency.id,
                'name': _(currency.name),
                'selected': currency.id == selected_currency_id,
            })

        options['currencies_selected'] = selected_currency_id
        options['currencies_selected_name'] = selected_currency_name



    #Override base method
    # def _build_column_dict(
    #         self, col_value, col_data,
    #         options=None, currency=False, digits=1,
    #         column_expression=None, has_sublines=False,
    #         report_line_id=None,
    # ):
    #     import datetime
    #
    #     if col_value is None and col_data is None:
    #         return {}
    #
    #     col_data = col_data or {}
    #     column_expression = column_expression or self.env['account.report.expression']
    #     options = options or {}
    #
    #     blank_if_zero = column_expression.blank_if_zero or col_data.get('blank_if_zero', False)
    #     figure_type = column_expression.figure_type or col_data.get('figure_type', 'string')
    #
    #     expr = col_data.get('expression_label')
    #     is_amount_currency_col = (expr == 'amount_currency')
    #     is_balance_col = (expr == 'balance')
    #     if is_balance_col:
    #         print('1111111111111111')
    #
    #     company_currency = self.env.company.currency_id
    #
    #     # Determine final currency
    #     if is_amount_currency_col:
    #         final_currency = currency or company_currency
    #     else:
    #         # Use selected currency for formatting
    #         currency_data = options.get("currencies_selected")
    #         to_currency = self._extract_currency(currency_data)
    #         if not to_currency:
    #             to_currency = self.env['res.currency'].search(
    #                 [('name', '=', options.get('currencies_selected_name'))], limit=1)
    #         final_currency = to_currency or currency or company_currency
    #
    #         # Convert ONLY if this is NOT the balance column
    #         # if isinstance(col_value, (int, float)) and not is_balance_col:
    #         if isinstance(col_value, (int, float)):
    #             if final_currency.id != company_currency.id:
    #                 col_value = company_currency._convert(
    #                     col_value,
    #                     final_currency,
    #                     date=datetime.datetime.strptime(options['date']['date_to'], '%Y-%m-%d').date()
    #                 )
    #
    #     # Build format_params
    #     format_params = {}
    #     if figure_type == 'monetary':
    #         format_params['currency_id'] = final_currency.id
    #     elif figure_type in ('float', 'percentage'):
    #         format_params['digits'] = digits
    #
    #     data = {
    #         'auditable': col_value is not None and column_expression.auditable,
    #         'blank_if_zero': blank_if_zero,
    #         'column_group_key': col_data.get('column_group_key'),
    #         'currency': final_currency,
    #         'currency_symbol': final_currency.symbol if options.get('multi_currency') else None,
    #         'digits': digits,
    #         'expression_label': expr,
    #         'figure_type': figure_type,
    #         'green_on_positive': column_expression.green_on_positive,
    #         'has_sublines': has_sublines,
    #         'is_zero': col_value is None or (
    #                 isinstance(col_value, (int, float))
    #                 and figure_type in NUMBER_FIGURE_TYPES
    #                 and self._is_value_zero(col_value, figure_type, format_params)
    #         ),
    #         'name': self._format_value(
    #             options,
    #             col_value,
    #             figure_type,
    #             format_params=format_params,
    #             blank_if_zero=blank_if_zero
    #         ),
    #         'no_format': col_value,
    #         'report_line_id': report_line_id,
    #         'sortable': col_data.get('sortable', False),
    #     }
    #
    #     return data

    # def _build_column_dict(
    #         self, col_value, col_data,
    #         options=None, currency=False, digits=1,
    #         column_expression=None, has_sublines=False,
    #         report_line_id=None,
    # ):
    #     # Empty column
    #     if col_value is None and col_data is None:
    #         return {}
    #
    #     col_data = col_data or {}
    #     column_expression = column_expression or self.env['account.report.expression']
    #     options = options or {}
    #
    #     blank_if_zero = column_expression.blank_if_zero or col_data.get('blank_if_zero', False)
    #     figure_type = column_expression.figure_type or col_data.get('figure_type', 'string')
    #
    #     expr = col_data.get('expression_label')
    #     is_amount_currency_col = (expr == 'amount_currency')
    #     # is_balance_col = (expr == 'balance')
    #
    #     # Determine currency for formatting
    #     if is_amount_currency_col:
    #         # Keep original currency for Amount Currency column
    #         final_currency = currency or self.env.company.currency_id
    #     else:
    #         # Use report filter currency for other columns
    #         currency_data = options.get("currencies_selected")
    #         to_currency = self._extract_currency(currency_data)
    #         if not to_currency:
    #             to_currency = self.env['res.currency'].search(
    #                 [('name', '=', options.get('currencies_selected_name'))], limit=1)
    #         final_currency = to_currency or currency or self.env.company.currency_id
    #         # Convert value
    #         if isinstance(col_value, (int, float)):
    #             # Use company's currency for conversion base
    #             company_currency = self.env.company.currency_id
    #             col_value = company_currency._convert(col_value, final_currency,
    #                                                   date=datetime.datetime.strptime(options['date']['date_to'],
    #                                                                                   '%Y-%m-%d').date())
    #
    #     # Build format_params for Odoo18 _format_value
    #     format_params = {}
    #     if figure_type == 'monetary':
    #         format_params['currency_id'] = final_currency.id
    #     elif figure_type in ('float', 'percentage'):
    #         format_params['digits'] = digits
    #
    #     data = {
    #         'auditable': col_value is not None and column_expression.auditable,
    #         'blank_if_zero': blank_if_zero,
    #         'column_group_key': col_data.get('column_group_key'),
    #         'currency': final_currency,
    #         'currency_symbol': final_currency.symbol if options.get('multi_currency') else None,
    #         'digits': digits,
    #         'expression_label': expr,
    #         'figure_type': figure_type,
    #         'green_on_positive': column_expression.green_on_positive,
    #         'has_sublines': has_sublines,
    #         'is_zero': col_value is None or (
    #                 isinstance(col_value, (int, float))
    #                 and figure_type in NUMBER_FIGURE_TYPES
    #                 and self._is_value_zero(col_value, figure_type, format_params)
    #         ),
    #         'name': self._format_value(
    #             options,
    #             col_value,
    #             figure_type,
    #             format_params=format_params,
    #             blank_if_zero=blank_if_zero
    #         ),
    #         'no_format': col_value,
    #         'report_line_id': report_line_id,
    #         'sortable': col_data.get('sortable', False),
    #     }
    #
    #     return data

    #Override base method
    def _init_options_rounding_unit(self, options, previous_options=None):
        default = 'decimals'

        if previous_options:
            options['rounding_unit'] = previous_options.get('rounding_unit', default)
        else:
            options['rounding_unit'] = default

        currency_data = previous_options.get('currencies_selected')
        old_name = previous_options.get('currencies_selected_name')

        currency_obj = self._extract_currency(currency_data)

        if not currency_obj and old_name:
            currency_obj = self.env['res.currency'].search([('name', '=', old_name)], limit=1)

        if not currency_obj:
            currency_obj = self.env.company.currency_id

        options['rounding_unit_names'] = self._get_rounding_unit_names(currency_obj)


    #Override base method
    def _get_rounding_unit_names(self,currency_obj):
        if currency_obj:
            currency_symbol = currency_obj.symbol
        else:
            currency_symbol = self.env.company.currency_id.symbol

        rounding_unit_names = [
            ('decimals', '.%s' % currency_symbol),
            ('units', '%s' % currency_symbol),
            ('thousands', 'K%s' % currency_symbol),
            ('millions', 'M%s' % currency_symbol),
        ]

        # We want to add 'lakhs' for Indian Rupee
        if (self.env.company.currency_id == self.env.ref('base.INR')):
            # We want it between 'thousands' and 'millions'
            rounding_unit_names.insert(3, ('lakhs', 'L%s' % currency_symbol))

        return dict(rounding_unit_names)



class AgedPartnerBalanceCustomHandler(models.AbstractModel):
    _inherit = "account.aged.partner.balance.report.handler"


    def _get_custom_display_config(self):
        config = super()._get_custom_display_config()

        # Only extend AgedPartnerBalanceFilters, do NOT override whole component!
        config['templates'].update({
            'account_reports.AgedPartnerBalanceFilters':
                'mh_multi_currency_accounting_reports.currencyReportFiltersCustomizable',
        })

        return config


    # ---------------------------------------------------------------------
    # Inject custom filters in Odoo18-style
    # ---------------------------------------------------------------------
    def _custom_options_initializer(self, report, options, previous_options):
        # call super first
        super()._custom_options_initializer(report, options, previous_options=previous_options)

        # Keep track of columns to hide
        hidden_columns = set()

        # Multi-currency flag (needed by the filter template to show the "Show Currency" option)
        options['multi_currency'] = report.env.user.has_group('base.group_multi_currency')

        # Respect previously chosen "show_currency" (frontend sends it in previous_options)
        options['show_currency'] = options['multi_currency'] and (previous_options or {}).get('show_currency', False)
        if not options['show_currency']:
            hidden_columns.update(['amount_currency', 'currency'])

        # Respect previously chosen "show_account"
        options['show_account'] = (previous_options or {}).get('show_account', False)
        if not options['show_account']:
            hidden_columns.add('account_name')

        # Remove hidden columns from options['columns'] (if present)
        if 'columns' in options and options['columns']:
            options['columns'] = [
                column for column in options['columns']
                if column.get('expression_label') not in hidden_columns
            ]

        # Keep ordering and aging settings as Odoo expects
        default_order_column = {
            'expression_label': 'invoice_date',
            'direction': 'ASC',
        }
        options['order_column'] = (previous_options or {}).get('order_column') or default_order_column
        options['aging_based_on'] = (previous_options or {}).get('aging_based_on') or 'base_on_maturity_date'
        options['aging_interval'] = (previous_options or {}).get('aging_interval') or 30

        # Set aging column names
        interval = options['aging_interval']
        for column in options.get('columns', []):
            expr = column.get('expression_label', '')
            if expr.startswith('period'):
                try:
                    period_number = int(expr.replace('period', '')) - 1
                except Exception:
                    continue
                if 0 <= period_number < 4:
                    column['name'] = f'{interval * period_number + 1}-{interval * (period_number + 1)}'

        # --- Now add your currencies dropdown data (only if multi_currency enabled) ---
        if not options['multi_currency']:
            # ensure keys are not present when multi-currency is disabled
            options.pop('currencies', None)
            options.pop('currencies_selected', None)
            options.pop('currencies_selected_name', None)
            return

        # Read previously selected currency id (frontend sends this in previous_options)
        selected_currency_id = (previous_options or {}).get('currencies_selected')

        currencies = self.env['res.currency'].search([], order='id')
        options['currencies'] = [{
            'id': c.id,
            'name': c.name,
            'selected': bool(selected_currency_id and c.id == selected_currency_id),
        } for c in currencies]

        # Keep selected name and id consistent so the button label persists
        if selected_currency_id:
            options['currencies_selected_name'] = self.env['res.currency'].browse(selected_currency_id).name
            options['currencies_selected'] = int(selected_currency_id)
        else:
            options['currencies_selected_name'] = "All"
            options['currencies_selected'] = False


class PartnerLedgerCustomHandler(models.AbstractModel):
    _inherit = "account.partner.ledger.report.handler"

    def _extract_currency(self, currency_data):
        """Accepts: int id OR dict {'id': x, 'name': y}
           Returns: currency record OR False
        """
        if not currency_data:
            return False

        # case 1: already an int ID
        if isinstance(currency_data, int):
            return self.env['res.currency'].browse(currency_data)

        # case 2: dict {'id':.., 'name':..}
        if isinstance(currency_data, dict):
            cid = currency_data.get('id')
            return self.env['res.currency'].browse(cid) if cid else False

        return False


    def _get_report_line_partners(self, options, partner, partner_values, level_shift=0):
        company_currency = self.env.company.currency_id
        currency_data = options.get("currencies_selected")
        to_currency = self._extract_currency(currency_data)

        partner_data = next(iter(partner_values.values()))
        unfoldable = not company_currency.is_zero(partner_data.get('debit', 0) or partner_data.get('credit', 0))
        column_values = []
        report = self.env['account.report'].browse(options['report_id'])

        for column in options['columns']:
            col_expr_label = column['expression_label']
            value = partner_values[column['column_group_key']].get(col_expr_label)

            # Convert to selected currency if needed
            if to_currency and col_expr_label not in ('amount_currency', 'quantity'):
                value = company_currency._convert(value, to_currency, self.env.company, fields.Date.today())

            # Pass target currency to _build_column_dict
            column_values.append(report._build_column_dict(
                value, column, options=options, currency=to_currency
            ))

            unfoldable = unfoldable or (
                        col_expr_label in ('debit', 'credit', 'amount') and not company_currency.is_zero(value))

        line_id = report._get_generic_line_id('res.partner', partner.id) if partner else report._get_generic_line_id(
            'res.partner', None, markup='no_partner')

        return {
            'id': line_id,
            'name': partner.name if partner else self._get_no_partner_line_label(),
            'columns': column_values,
            'level': 1 + level_shift,
            'trust': partner.trust if partner else None,
            'unfoldable': unfoldable,
            'unfolded': line_id in options['unfolded_lines'] or options['unfold_all'],
            'expand_function': '_report_expand_unfoldable_line_partner_ledger',
        }

    def _get_report_line_total(self, options, totals_by_column_group):
        company_currency = self.env.company.currency_id
        currency_data = options.get("currencies_selected")
        to_currency = self._extract_currency(currency_data)

        column_values = []
        report = self.env['account.report'].browse(options['report_id'])

        for column in options['columns']:
            col_value = totals_by_column_group[column['column_group_key']].get(column['expression_label'])

            # Convert to selected currency
            if to_currency and column['expression_label'] not in ('amount_currency', 'quantity'):
                col_value = company_currency._convert(col_value, to_currency, self.env.company, fields.Date.today())

            # Pass currency for display
            column_values.append(report._build_column_dict(
                col_value, column, options=options, currency=to_currency
            ))

        return {
            'id': report._get_generic_line_id(None, None, markup='total'),
            'name': _('Total'),
            'level': 1,
            'columns': column_values,
        }

    def _get_report_line_move_line(self, options, aml_query_result, partner_line_id, init_bal_by_col_group,
                                   level_shift=0):
        # Determine caret type
        caret_type = 'account.payment' if aml_query_result.get('payment_id') else 'account.move.line'

        columns = []
        report = self.env['account.report'].browse(options['report_id'])

        # Get the selected currency for conversion
        currency_data = options.get("currencies_selected")
        to_currency = self._extract_currency(currency_data)

        for column in options['columns']:
            col_expr_label = column['expression_label']
            col_value = aml_query_result.get(col_expr_label) if column['column_group_key'] == aml_query_result[
                'column_group_key'] else None

            if col_value is None:
                columns.append(report._build_column_dict(None, None))
                continue

            currency = False

            # amount_currency column should remain unchanged
            if col_expr_label == 'amount_currency':
                currency = self.env['res.currency'].browse(aml_query_result['currency_id'])
            else:
                # Convert other monetary columns to selected currency
                if to_currency and col_expr_label in ('debit', 'credit', 'balance', 'amount'):
                    from_currency = self.env.company.currency_id
                    col_value = from_currency._convert(
                        col_value,
                        to_currency,
                        self.env.company,
                        aml_query_result.get('date') or fields.Date.today()
                    )
                    currency = to_currency

                # If balance, add initial balance
                if col_expr_label == 'balance':
                    col_value += init_bal_by_col_group[column['column_group_key']]

            columns.append(report._build_column_dict(col_value, column, options=options, currency=currency))

        return {
            'id': report._get_generic_line_id(
                'account.move.line',
                aml_query_result['id'],
                parent_line_id=partner_line_id,
                markup=aml_query_result.get('partial_id'),
            ),
            'parent_id': partner_line_id,
            'name': self._format_aml_name(
                aml_query_result['name'],
                aml_query_result['ref'],
                aml_query_result.get('move_name')
            ),
            'columns': columns,
            'caret_options': caret_type,
            'level': 3 + level_shift,
        }


    def _get_custom_display_config(self):
        return {
            'templates': {
                'AccountReportFilters': 'mh_multi_currency_accounting_reports.currencyReportFiltersCustomizablePL',
            },
        }


    def _custom_options_initializer(self, report, options, previous_options):
        super()._custom_options_initializer(report, options, previous_options=previous_options)

        # ----------------------------------------------------------------------
        # DEFAULT PARTNER LEDGER LOGIC (unchanged)
        # ----------------------------------------------------------------------
        domain = []

        company_ids = report.get_report_company_ids(options)
        exch_code = self.env['res.company'].browse(company_ids).mapped('currency_exchange_journal_id')
        if exch_code:
            domain += ['!', '&', '&', '&', ('credit', '=', 0.0), ('debit', '=', 0.0),
                       ('amount_currency', '!=', 0.0), ('journal_id', 'in', exch_code.ids)]

        if options['export_mode'] == 'print' and options.get('filter_search_bar'):
            domain += [
                '|', ('matched_debit_ids.debit_move_id.partner_id.name', 'ilike', options['filter_search_bar']),
                '|', ('matched_credit_ids.credit_move_id.partner_id.name', 'ilike', options['filter_search_bar']),
                ('partner_id.name', 'ilike', options['filter_search_bar']),
            ]

        options['forced_domain'] = options.get('forced_domain', []) + domain

        # ----------------------------------------------------------------------
        #  MULTI CURRENCY ENABLE / DISABLE (default Odoo)
        # ----------------------------------------------------------------------
        if self.env.user.has_group('base.group_multi_currency'):
            options['multi_currency'] = True
        else:
            options['multi_currency'] = False
            options['columns'] = [
                col for col in options['columns']
                if col['expression_label'] != 'amount_currency'
            ]

        # ----------------------------------------------------------------------
        # YOUR CUSTOM CURRENCY DROPDOWN LOGIC
        # ----------------------------------------------------------------------
        if options.get('multi_currency'):

            # Read selection from previous options (sent from JS)
            selected_currency_id = (previous_options or {}).get("currencies_selected")

            # Load all currencies
            currencies = self.env['res.currency'].search([])

            options['currencies'] = []
            for c in currencies:
                options['currencies'].append({
                    'id': c.id,
                    'name': c.name,
                    'selected': c.id == selected_currency_id,
                })

            # Selected name (button label)
            if selected_currency_id:
                options['currencies_selected_name'] = self.env['res.currency'].browse(
                    selected_currency_id
                ).name
            else:
                options['currencies_selected_name'] = "All"

            # Store selected currency ID
            options['currencies_selected'] = selected_currency_id

        # ----------------------------------------------------------------------
        # DEFAULT HIDE ACCOUNT / HIDE DEBIT CREDIT / SEND BUTTON (unchanged)
        # ----------------------------------------------------------------------
        if not self.env.ref('account_reports.customer_statement_report', raise_if_not_found=False):
            columns_to_hide = []

            options['hide_account'] = (previous_options or {}).get('hide_account', False)
            if options['hide_account']:
                columns_to_hide += ['journal_code', 'account_code', 'matching_number']

            options['hide_debit_credit'] = (previous_options or {}).get('hide_debit_credit', False)
            if options['hide_debit_credit']:
                columns_to_hide += ['debit', 'credit']
            else:
                columns_to_hide += ['amount']

            # Remove columns accordingly
            options['columns'] = [
                col for col in options['columns']
                if col['expression_label'] not in columns_to_hide
            ]

            options['buttons'].append({
                'name': _('Send'),
                'action': 'action_send_statements',
                'sequence': 90,
                'always_show': True,
            })

