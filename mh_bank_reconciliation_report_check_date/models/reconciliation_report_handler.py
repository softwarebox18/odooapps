from datetime import date
import logging
from odoo import models, fields, _
from odoo.exceptions import UserError
from odoo.tools import SQL

_logger = logging.getLogger(__name__)


class AccountBankReconciliationReportHandler(models.AbstractModel):
    _inherit = "account.bank.reconciliation.report.handler"

    def _build_custom_engine_result(
        self, date=None, label=None, amount_currency=None,
        amount_currency_currency_id=None, currency=None,
        amount=0, amount_currency_id=None, has_sublines=False,
        check_date=None, check_number=None,
    ):
        """Extend original method to also return check_date and check_number (keeps compatibility)."""
        res = super()._build_custom_engine_result(
            date=date,
            label=label,
            amount_currency=amount_currency,
            amount_currency_currency_id=amount_currency_currency_id,
            currency=currency,
            amount=amount,
            amount_currency_id=amount_currency_id,
            has_sublines=has_sublines,
        )
        res["check_date"] = check_date
        res["check_number"] = check_number
        return res

    def _custom_options_initializer(self, report, options, previous_options):
        """Insert Check Date and Check Number columns after the Label column."""
        super()._custom_options_initializer(report, options, previous_options=previous_options)

        # Avoid double insertion
        if any(col.get("expression_label") in ("check_date", "check_number") for col in options.get("columns", [])):
            return

        new_columns = []
        inserted = False
        for col in options.get("columns", []):
            new_columns.append(col)
            if not inserted and (col.get("expression_label") == "label" or col.get("name") == _("Label")):
                # Clone structure from label column
                check_date_col = col.copy()
                check_date_col.update({
                    "name": _("Check Date"),
                    "expression_label": "check_date",
                    "sortable": False,
                })
                new_columns.append(check_date_col)

                check_number_col = col.copy()
                check_number_col.update({
                    "name": _("Check Number"),
                    "expression_label": "check_number",
                    "sortable": False,
                })
                new_columns.append(check_number_col)
                inserted = True

        if not inserted:
            # Fallback if no label column was found
            for lbl, expr in [(_("Check Date"), "check_date"), (_("Check Number"), "check_number")]:
                fallback = (options["columns"][-1].copy() if options.get("columns") else {"column_group_key": 0})
                fallback.update({"name": lbl, "expression_label": expr, "sortable": False})
                new_columns.append(fallback)

        options["columns"] = new_columns

    def _custom_line_postprocessor(self, report, options, lines):
        """Populate Check Date and Check Number columns per line."""
        lines = super()._custom_line_postprocessor(report, options, lines)

        # find column indices
        check_date_idx = check_number_idx = None
        for idx, col in enumerate(options.get("columns", [])):
            if col.get("expression_label") == "check_date":
                check_date_idx = idx
            if col.get("expression_label") == "check_number":
                check_number_idx = idx

        if check_date_idx is None and check_number_idx is None:
            return lines

        for line in lines:
            if not isinstance(line, dict) or "columns" not in line:
                continue

            try:
                model, model_id = report._get_model_info_from_id(line["id"])
            except Exception:
                continue

            if model != "account.move.line" or not model_id:
                continue

            aml = self.env["account.move.line"].browse(model_id)
            pay = aml.payment_id if aml.exists() else False

            # --- Check Date ---
            if check_date_idx is not None:
                check_date_value = pay.check_date if pay and pay.check_date else ""
                formatted_date = ""
                if check_date_value:
                    try:
                        formatted_date = report.format_value(options, check_date_value, figure_type="date")
                    except Exception:
                        formatted_date = str(check_date_value)
                while len(line["columns"]) <= check_date_idx:
                    line["columns"].append({"name": ""})
                line["columns"][check_date_idx] = {"name": formatted_date}

            # --- Check Number ---
            if check_number_idx is not None:
                check_number_value = pay.check_number if pay and pay.check_number else ""
                while len(line["columns"]) <= check_number_idx:
                    line["columns"].append({"name": ""})
                line["columns"][check_number_idx] = {"name": str(check_number_value)}

        return lines

############################################################################################


# class AccountBankReconciliationReportHandler(models.AbstractModel):
#     _inherit = "account.bank.reconciliation.report.handler"
#
#     def _build_custom_engine_result(
#         self, date=None, label=None, amount_currency=None,
#         amount_currency_currency_id=None, currency=None,
#         amount=0, amount_currency_id=None, has_sublines=False,
#         check_date=None, check_number=None,
#     ):
#         """Extend original method to also return check_date and check_number (keeps compatibility)."""
#         res = super()._build_custom_engine_result(
#             date=date,
#             label=label,
#             amount_currency=amount_currency,
#             amount_currency_currency_id=amount_currency_currency_id,
#             currency=currency,
#             amount=amount,
#             amount_currency_id=amount_currency_id,
#             has_sublines=has_sublines,
#         )
#         res["check_date"] = check_date
#         res["check_number"] = check_number
#         return res
#
#     def _custom_options_initializer(self, report, options, previous_options):
#         """Insert Check Date and Check Number columns after the Label column."""
#         super()._custom_options_initializer(report, options, previous_options=previous_options)
#
#         # Avoid double insertion
#         if any(col.get("expression_label") in ("check_date", "check_number") for col in options.get("columns", [])):
#             return
#
#         new_columns = []
#         inserted = False
#         for col in options.get("columns", []):
#             new_columns.append(col)
#             if not inserted and (col.get("expression_label") == "label" or col.get("name") == _("Label")):
#                 # Clone structure from label column
#                 check_date_col = col.copy()
#                 check_date_col.update({
#                     "name": _("Check Date"),
#                     "expression_label": "check_date",
#                     "sortable": False,
#                 })
#                 new_columns.append(check_date_col)
#
#                 check_number_col = col.copy()
#                 check_number_col.update({
#                     "name": _("Check Number"),
#                     "expression_label": "check_number",
#                     "sortable": False,
#                 })
#                 new_columns.append(check_number_col)
#                 inserted = True
#
#         if not inserted:
#             # Fallback if no label column was found
#             for lbl, expr in [(_("Check Date"), "check_date"), (_("Check Number"), "check_number")]:
#                 fallback = (options["columns"][-1].copy() if options.get("columns") else {"column_group_key": 0})
#                 fallback.update({"name": lbl, "expression_label": expr, "sortable": False})
#                 new_columns.append(fallback)
#
#         options["columns"] = new_columns
#
#     def _custom_line_postprocessor(self, report, options, lines):
#         """Populate Check Date and Check Number columns per line."""
#         lines = super()._custom_line_postprocessor(report, options, lines)
#
#         # find column indices
#         check_date_idx = check_number_idx = None
#         for idx, col in enumerate(options.get("columns", [])):
#             if col.get("expression_label") == "check_date":
#                 check_date_idx = idx
#             if col.get("expression_label") == "check_number":
#                 check_number_idx = idx
#
#         if check_date_idx is None and check_number_idx is None:
#             return lines
#
#         for line in lines:
#             if not isinstance(line, dict) or "columns" not in line:
#                 continue
#
#             try:
#                 model, model_id = report._get_model_info_from_id(line["id"])
#             except Exception:
#                 continue
#
#             if model != "account.move.line" or not model_id:
#                 continue
#
#             aml = self.env["account.move.line"].browse(model_id)
#             pay = aml.payment_id if aml.exists() else False
#
#             # --- Check Date ---
#             if check_date_idx is not None:
#                 check_date_value = pay.check_date if pay and pay.check_date else ""
#                 formatted_date = ""
#                 if check_date_value:
#                     try:
#                         formatted_date = report.format_value(options, check_date_value, figure_type="date")
#                     except Exception:
#                         formatted_date = str(check_date_value)
#                 while len(line["columns"]) <= check_date_idx:
#                     line["columns"].append({"name": ""})
#                 line["columns"][check_date_idx] = {"name": formatted_date}
#
#             # --- Check Number ---
#             if check_number_idx is not None:
#                 check_number_value = pay.check_number if pay and pay.check_number else ""
#                 while len(line["columns"]) <= check_number_idx:
#                     line["columns"].append({"name": ""})
#                 line["columns"][check_number_idx] = {"name": str(check_number_value)}
#
#         return lines
############################################################################################



# class AccountBankReconciliationReportHandler(models.AbstractModel):
#     _inherit = "account.bank.reconciliation.report.handler"
#
#     def _build_custom_engine_result(
#         self, date=None, label=None, amount_currency=None,
#         amount_currency_currency_id=None, currency=None,
#         amount=0, amount_currency_id=None, has_sublines=False,
#         check_date=None,
#     ):
#         """Extend original method to also return check_date (keeps compatibility)."""
#         res = super()._build_custom_engine_result(
#             date=date,
#             label=label,
#             amount_currency=amount_currency,
#             amount_currency_currency_id=amount_currency_currency_id,
#             currency=currency,
#             amount=amount,
#             amount_currency_id=amount_currency_id,
#             has_sublines=has_sublines,
#         )
#         # safe to add additional key — report engine will ignore unknown keys but we may use it later
#         res["check_date"] = check_date
#         return res
#
#     def _custom_options_initializer(self, report, options, previous_options):
#         """Insert Check Date column after the Label column, cloning structure from the Label column."""
#         super()._custom_options_initializer(report, options, previous_options=previous_options)
#
#         # Avoid double insertion
#         if any(col.get("expression_label") == "check_date" for col in options.get("columns", [])):
#             return
#
#         new_columns = []
#         inserted = False
#         for col in options.get("columns", []):
#             new_columns.append(col)
#             # Heuristic: find the label column by expression_label 'label' OR by column name 'Label'
#             if not inserted and (col.get("expression_label") in ("label",) or col.get("name") == _("Label")):
#                 # clone the column dict to keep keys like column_group_key etc.
#                 new_col = col.copy()
#                 new_col.update({
#                     "name": _("Check Date"),
#                     "expression_label": "check_date",
#                     # This column is display-only here: disabling sorting avoids engine looking for expressions.
#                     "sortable": False,
#                 })
#                 new_columns.append(new_col)
#                 inserted = True
#
#         # If we didn't find a label column, append at the end
#         if not inserted:
#             # try to clone last column to have necessary keys, otherwise create minimal safe structure
#             if options.get("columns"):
#                 fallback = options["columns"][-1].copy()
#                 fallback.update({
#                     "name": _("Check Date"),
#                     "expression_label": "check_date",
#                     "sortable": False,
#                 })
#             else:
#                 fallback = {"name": _("Check Date"), "expression_label": "check_date", "sortable": False, "column_group_key": 0}
#             new_columns.append(fallback)
#
#         options["columns"] = new_columns
#
#     def _custom_line_postprocessor(self, report, options, lines):
#         """
#         Called after lines are built. We will populate the 'Check Date' column here.
#         This keeps the SQL/query untouched and is robust across Odoo upgrades.
#         """
#         # First call parent to keep original behavior
#         lines = super()._custom_line_postprocessor(report, options, lines)
#
#         # find index of our 'check_date' column in options
#         check_date_col_index = None
#         for idx, col in enumerate(options.get("columns", [])):
#             # prefer expression_label if present
#             if col.get("expression_label") == "check_date":
#                 check_date_col_index = idx
#                 break
#             # fallback by header name match (in case expression_label differs)
#             if str(col.get("name")).strip().lower() == str(_("Check Date")).strip().lower():
#                 check_date_col_index = idx
#                 break
#
#         # nothing to do if check_date column not present
#         if check_date_col_index is None:
#             return lines
#
#         # Loop through built lines and set the value when model == account.move.line
#         for line in lines:
#             # defensive checks: line must be dict and have id and columns
#             if not isinstance(line, dict):
#                 continue
#             if "columns" not in line or not isinstance(line["columns"], list):
#                 continue
#
#             # Get model and model id from the line id
#             try:
#                 model, model_id = report._get_model_info_from_id(line["id"])
#             except Exception:
#                 # if the helper fails for some line id, skip it
#                 continue
#
#             if model != "account.move.line" or not model_id:
#                 # ensure the line still has same column count: insert blank cell if shorter
#                 # Some lines might not have enough columns (depending on engine); ensure length
#                 if len(line["columns"]) <= check_date_col_index:
#                     # pad with empty columns up to required index
#                     while len(line["columns"]) <= check_date_col_index:
#                         line["columns"].append({"name": ""})
#                 # leave non-move.line lines blank for this column
#                 # (we don't want to overwrite other columns)
#                 continue
#
#             # At this point model is account.move.line and model_id is the aml id
#             aml = self.env["account.move.line"].browse(model_id)
#             if not aml.exists():
#                 check_date_value = ""
#             else:
#                 # fetch from related payment
#                 pay = aml.payment_id
#                 check_date_value = pay.check_date if (pay and pay.check_date) else ""
#
#             # format date nicely using report.format_value if possible, otherwise str()
#             formatted = ""
#             if check_date_value:
#                 try:
#                     # report.format_value can format dates; use it if available
#                     formatted = report.format_value(options, check_date_value, figure_type="date")
#                 except Exception:
#                     formatted = str(check_date_value)
#
#             # ensure line has enough columns; if not, pad with blank columns
#             while len(line["columns"]) <= check_date_col_index:
#                 line["columns"].append({"name": ""})
#
#             # update the exact column cell
#             # keep other keys in the cell (like 'class' or 'auditable'), only set name
#             try:
#                 cell = line["columns"][check_date_col_index]
#                 if isinstance(cell, dict):
#                     cell.update({"name": formatted})
#                 else:
#                     # cell might be primitive (unlikely) — replace with dict
#                     line["columns"][check_date_col_index] = {"name": formatted}
#             except Exception as e:
#                 _logger.exception("Failed to set check_date on report line %s: %s", line.get("id"), e)
#
#         return lines


