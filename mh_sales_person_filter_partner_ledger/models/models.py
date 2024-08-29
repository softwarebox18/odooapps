# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools, _

class AccountMoveLineSP(models.Model):
    _inherit = 'account.move.line'

    # sales_person_id = fields.Many2one('res.users',string='Salesperson')

    sales_person_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        compute='_compute_sales_person_id',
        store=True,
        readonly=True
    )

    @api.depends('move_id.move_type', 'sale_line_ids.order_id.user_id', 'move_id.invoice_user_id')
    def _compute_sales_person_id(self):
        for line in self:
            # Check if the move type is 'out_invoice' (customer invoice)
            if line.move_id.move_type == 'out_invoice':
                if not line.sale_line_ids:
                    # Set the `sales_person_id` based on the move's salesperson or the creator
                    line.sales_person_id = line.move_id.invoice_user_id or line.move_id.create_uid
                else:
                    # Set the `sales_person_id` based on the sale order's user_id
                    line.sales_person_id = line.sale_line_ids[0].order_id.user_id
            else:
                # Clear the sales_person_id for other types of moves
                line.sales_person_id = False

    sales_person = fields.Char(string='Salesperson',related='sales_person_id.name',store=True)

class AccountReportInheritSP(models.Model):
    _inherit = "account.report"

    filter_sales_person = fields.Boolean(
        string="Sales Person",
        compute=lambda x: x._compute_report_option_filter('filter_sales_person'), readonly=False, store=True,
        depends=['root_report_id', 'section_main_report_ids'],
    )

    @api.onchange('filter_sales_person')
    def _onchange_enable_sales_person(self):
        # Identify columns to keep and remove
        columns_to_keep = [(4, col.id, 0) for col in self.column_ids if col.name != 'Sale Person']
        columns_to_remove = [(2, col.id, 0) for col in self.column_ids if col.name == 'Sale Person']

        if self.filter_sales_person:
            # Add 'Sale Person' column if not already present
            if not any(col.name == 'Sale Person' for col in self.column_ids):
                columns_to_keep.append((0, 0, {
                    'name': 'Sale Person',
                    'expression_label': 'sales_person',
                    'figure_type': 'string',
                    'sequence': 1,
                }))

        # Update column_ids with filtered and new columns
        self.column_ids = columns_to_remove + columns_to_keep


    ####################################################
    # OPTIONS: sales person
    ####################################################

    def _init_options_salesperson(self, options, previous_options=None):
        if not self.filter_sales_person:
            return

        options['salesperson'] = True
        previous_salesperson_ids = previous_options and previous_options.get('salesperson_ids') or []

        selected_salesperson_ids = [int(salesperson) for salesperson in previous_salesperson_ids]
        # Using search instead of browse so that record rules apply and filter out the ones the user does not have access to
        selected_salespersons = selected_salesperson_ids and self.env['res.users'].with_context(active_test=False).search([('id', 'in', selected_salesperson_ids)]) or self.env['res.users']
        options['selected_salesperson_ids'] = selected_salespersons.mapped('name')
        options['salesperson_ids'] = selected_salespersons.ids

    @api.model
    def _get_options_salesperson_domain(self, options):
        domain = []
        if options.get('salesperson_ids'):
            salesperson_ids = [int(salesperson) for salesperson in options['salesperson_ids']]
            domain.append(('sales_person_id', 'in', salesperson_ids))
            # print('1111111111111',domain)
        return domain

    def _get_options_domain(self, options, date_scope):
        domain = super(AccountReportInheritSP, self)._get_options_domain(options, date_scope)
        domain += self._get_options_salesperson_domain(options)  # Add salesperson domain
        return domain


class PartnerLedgerCustomHandlerSP(models.AbstractModel):
    _inherit = 'account.partner.ledger.report.handler'

    def _get_report_line_move_line(self, options, aml_query_result, partner_line_id, init_bal_by_col_group, level_shift=0):
        if aml_query_result['payment_id']:
            caret_type = 'account.payment'
        else:
            caret_type = 'account.move.line'

        # Check if the Sales Person filter is enabled
        filter_sales_person = options.get('salesperson', False)
        if not filter_sales_person:
            options['columns'] = [col for col in options['columns'] if col['name'] != 'Sale Person']

        columns = []
        report = self.env['account.report'].browse(options['report_id'])

        for column in options['columns']:
            col_expr_label = column['expression_label']
            # print('11111111111111',col_expr_label,column['column_group_key'],aml_query_result['column_group_key'])
            col_value = aml_query_result[col_expr_label] if column['column_group_key'] == aml_query_result['column_group_key'] else None

            if col_value is None:
                columns.append(report._build_column_dict(None, None))
            else:
                if col_expr_label == 'balance':
                    col_value += init_bal_by_col_group[column['column_group_key']]

                if col_expr_label == 'amount_currency':
                    currency = self.env['res.currency'].browse(aml_query_result['currency_id'])

                    if currency == self.env.company.currency_id:
                        col_value = ''

                columns.append(report._build_column_dict(col_value, column, options=options))

        return {
            'id': report._get_generic_line_id('account.move.line', aml_query_result['id'], parent_line_id=partner_line_id),
            'parent_id': partner_line_id,
            'name': self._format_aml_name(aml_query_result['name'], aml_query_result['ref'], aml_query_result['move_name']),
            'columns': columns,
            'caret_options': caret_type,
            'level': 3 + level_shift,
        }

    def _get_aml_values(self, options, partner_ids, offset=0, limit=None):
        # Inherit the original method and add the 'sales_person_id' field to the query
        # rslt = super(PartnerLedgerCustomHandlerSP, self)._get_aml_values(options, partner_ids, offset, limit)
        rslt = {partner_id: [] for partner_id in partner_ids}
        partner_ids_wo_none = [x for x in partner_ids if x]
        directly_linked_aml_partner_clauses = []
        directly_linked_aml_partner_params = []
        indirectly_linked_aml_partner_params = []

        indirectly_linked_aml_partner_clause = 'aml_with_partner.partner_id IS NOT NULL'
        if None in partner_ids:
            directly_linked_aml_partner_clauses.append('account_move_line.partner_id IS NULL')
        if partner_ids_wo_none:
            directly_linked_aml_partner_clauses.append('account_move_line.partner_id IN %s')
            directly_linked_aml_partner_params.append(tuple(partner_ids_wo_none))
            indirectly_linked_aml_partner_clause = 'aml_with_partner.partner_id IN %s'
            indirectly_linked_aml_partner_params.append(tuple(partner_ids_wo_none))
        directly_linked_aml_partner_clause = '(' + ' OR '.join(directly_linked_aml_partner_clauses) + ')'

        ct_query = self.env['account.report']._get_query_currency_table(options)

        # Build the query dynamically based on the filter_sales_person option
        filter_sales_person = options.get('salesperson', False)
        sales_person_column = ''
        if filter_sales_person:
            sales_person_column = '''
                account_move_line.sales_person_id as sales_person_id,
                account_move_line.sales_person as sales_person,
            '''

        queries = []
        all_params = []
        lang = self.env.lang or get_lang(self.env).code
        journal_name = f"COALESCE(journal.name->>'{lang}', journal.name->>'en_US')" if \
            self.pool['account.journal'].name.translate else 'journal.name'
        account_name = f"COALESCE(account.name->>'{lang}', account.name->>'en_US')" if \
            self.pool['account.account'].name.translate else 'account.name'
        report = self.env.ref('account_reports.partner_ledger_report')
        for column_group_key, group_options in report._split_options_per_column_group(options).items():
            tables, where_clause, where_params = report._query_get(group_options, 'strict_range')

            all_params += [
                column_group_key,
                *where_params,
                *directly_linked_aml_partner_params,
                column_group_key,
                *indirectly_linked_aml_partner_params,
                *where_params,
                group_options['date']['date_from'],
                group_options['date']['date_to'],
            ]

            # Add sales_person_id to the query
            queries.append(f'''
                SELECT
                    account_move_line.id,
                    account_move_line.date_maturity,
                    account_move_line.name,
                    account_move_line.ref,
                    account_move_line.company_id,
                    account_move_line.account_id,
                    account_move_line.payment_id,
                    account_move_line.partner_id,
                    account_move_line.currency_id,
                    account_move_line.amount_currency,
                    account_move_line.matching_number,
                    {sales_person_column}  -- Conditionally add this line
                    --account_move_line.sales_person_id as sales_person_id,  -- Add this line
                    --account_move_line.sales_person as sales_person,  -- Add this line
                    COALESCE(account_move_line.invoice_date, account_move_line.date)                 AS invoice_date,
                    ROUND(account_move_line.debit * currency_table.rate, currency_table.precision)   AS debit,
                    ROUND(account_move_line.credit * currency_table.rate, currency_table.precision)  AS credit,
                    ROUND(account_move_line.balance * currency_table.rate, currency_table.precision) AS balance,
                    account_move.name                                                                AS move_name,
                    account_move.move_type                                                           AS move_type,
                    account.code                                                                     AS account_code,
                    {account_name}                                                                   AS account_name,
                    journal.code                                                                     AS journal_code,
                    {journal_name}                                                                   AS journal_name,
                    %s                                                                               AS column_group_key,
                    'directly_linked_aml'                                                            AS key
                FROM {tables}
                JOIN account_move ON account_move.id = account_move_line.move_id
                LEFT JOIN {ct_query} ON currency_table.company_id = account_move_line.company_id
                LEFT JOIN res_company company               ON company.id = account_move_line.company_id
                LEFT JOIN res_partner partner               ON partner.id = account_move_line.partner_id
                LEFT JOIN account_account account           ON account.id = account_move_line.account_id
                LEFT JOIN account_journal journal           ON journal.id = account_move_line.journal_id
                WHERE {where_clause} AND {directly_linked_aml_partner_clause}
                ORDER BY account_move_line.date, account_move_line.id
            ''')

            # Repeat the above block for the 'indirectly_linked_aml' section
            queries.append(f'''
                SELECT
                    account_move_line.id,
                    account_move_line.date_maturity,
                    account_move_line.name,
                    account_move_line.ref,
                    account_move_line.company_id,
                    account_move_line.account_id,
                    account_move_line.payment_id,
                    aml_with_partner.partner_id,
                    account_move_line.currency_id,
                    account_move_line.amount_currency,
                    account_move_line.matching_number,
                    {sales_person_column}  -- Conditionally add this line
                    --account_move_line.sales_person_id as sales_person_id,  -- Add this line
                    --account_move_line.sales_person as sales_person,  -- Add this line
                    COALESCE(account_move_line.invoice_date, account_move_line.date)                    AS invoice_date,
                    CASE WHEN aml_with_partner.balance > 0 THEN 0 ELSE ROUND(
                        partial.amount * currency_table.rate, currency_table.precision
                    ) END                                                                               AS debit,
                    CASE WHEN aml_with_partner.balance < 0 THEN 0 ELSE ROUND(
                        partial.amount * currency_table.rate, currency_table.precision
                    ) END                                                                               AS credit,
                    - sign(aml_with_partner.balance) * ROUND(
                        partial.amount * currency_table.rate, currency_table.precision
                    )                                                                                   AS balance,
                    account_move.name                                                                   AS move_name,
                    account_move.move_type                                                              AS move_type,
                    account.code                                                                        AS account_code,
                    {account_name}                                                                      AS account_name,
                    journal.code                                                                        AS journal_code,
                    {journal_name}                                                                      AS journal_name,
                    %s                                                                                  AS column_group_key,
                    'indirectly_linked_aml'                                                             AS key
                FROM {tables}
                    LEFT JOIN {ct_query} ON currency_table.company_id = account_move_line.company_id,
                    account_partial_reconcile partial,
                    account_move,
                    account_move_line aml_with_partner,
                    account_journal journal,
                    account_account account
                WHERE
                    (account_move_line.id = partial.debit_move_id OR account_move_line.id = partial.credit_move_id)
                    AND account_move_line.partner_id IS NULL
                    AND account_move.id = account_move_line.move_id
                    AND (aml_with_partner.id = partial.debit_move_id OR aml_with_partner.id = partial.credit_move_id)
                    AND {indirectly_linked_aml_partner_clause}
                    AND journal.id = account_move_line.journal_id
                    AND account.id = account_move_line.account_id
                    AND {where_clause}
                    AND partial.max_date BETWEEN %s AND %s
                ORDER BY account_move_line.date, account_move_line.id
            ''')

        # Finally, execute the query and return the results as before
        query = '(' + ') UNION ALL ('.join(queries) + ')'

        if offset:
            query += ' OFFSET %s '
            all_params.append(offset)

        if limit:
            query += ' LIMIT %s '
            all_params.append(limit)
        self._cr.execute(query, all_params)
        for aml_result in self._cr.dictfetchall():
            if aml_result['key'] == 'indirectly_linked_aml':
                if aml_result['partner_id'] in rslt:
                    rslt[aml_result['partner_id']].append(aml_result)

                if None in rslt:
                    rslt[None].append({
                        **aml_result,
                        'debit': aml_result['credit'],
                        'credit': aml_result['debit'],
                        'balance': -aml_result['balance'],
                    })
            else:
                rslt[aml_result['partner_id']].append(aml_result)
        return rslt













































# class AccountMoveSP(models.Model):
#     _inherit = 'account.move'
#
#     def action_post(self):
#         # Call the original `action_post` method to perform the standard operations
#         res = super(AccountMoveSP, self).action_post()
#
#         # Iterate through each move (invoice) being posted
#         for move in self:
#             # Check if the move type is 'out_invoice' (customer invoice)
#             if move.move_type == 'out_invoice':
#                 # Iterate through each line in the invoice
#                 for line in move.line_ids:
#                     # If the line is NOT linked to a sale order line
#                     if not line.sale_line_ids:
#                         # Set the `sales_person_id` based on the move's salesperson (if applicable)
#                         line.sales_person_id = move.invoice_user_id or move.create_uid
#                     else:
#                         # Set the `sales_person_id` based on the sale order's user_id
#                         line.sales_person_id = line.sale_line_ids[0].order_id.user_id
#
#         return res
