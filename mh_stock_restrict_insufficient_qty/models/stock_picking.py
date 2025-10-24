from odoo import models, api, exceptions, _
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError
from odoo.tools.float_utils import float_round

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def create(self, vals):
        record = super(StockPicking, self).create(vals)

        # Call stock availability check
        record._check_stock_availability()

        return record

    def _check_stock_availability(self):
        """
        Prevent creation if available stock is less than required
        for internal transfers or delivery orders.
        Only applies to users in the 'Salesman' group.
        """
        # Check if current user belongs to Salesman group
        if not self.env.user.has_group('mh_salesman_group.group_sale_salesman'):
            return  # Skip check for other users

        Quant = self.env['stock.quant'].with_context(active_test=False)
        for picking in self:
            # Only check for internal transfers or delivery orders
            if picking.picking_type_code in ['outgoing']:
                for move in picking.move_ids_without_package:
                    if move.product_id.type in ['combo','consu','service']:
                        available_qty = move.product_id.with_context(location=move.location_id.id).qty_available

                        product = move.product_id

                        reserved_qty = sum(Quant.search([
                            ('product_id', '=', move.product_id.id),
                            ('location_id', '=', move.location_id.id),
                        ]).mapped('reserved_quantity'))

                        # Reserved for this picking (exclude this from the "other" reserved)
                        reserved_for_this_picking  = move.product_uom_qty or 0.0

                        # Reserved by other pickings
                        reserved_by_others = reserved_qty - reserved_for_this_picking
                        real_available_qty = available_qty - abs(reserved_by_others)

                        print("Available Qty:", available_qty)
                        print("Reserved Qty:", reserved_qty)
                        print("Move Qty:", move.product_uom_qty)
                        print("Reserved by this picking:", reserved_for_this_picking)
                        print("Actually available:", real_available_qty)


                        # print("Available Qty:", available_qty)
                        # print("Reserved Qty:", reserved_qty)

                        # print('1111111111111',product,move.location_id)
                        # raise ValidationError('==========================')
                        if real_available_qty < move.product_uom_qty:
                        # if free_qty < 0:
                            raise UserError(_(
                                "Not enough stock for product '%s'.\n"
                                "Required: %s %s\n"
                                "Available in %s: %s %s"
                            ) % (
                                move.product_id.display_name,
                                move.product_uom_qty, move.product_uom.name,
                                move.location_id.display_name,
                                available_qty, move.product_uom.name
                            ))

            elif picking.picking_type_code == 'internal':
                # ---- Internal transfer logic ----
                for move in picking.move_ids_without_package:
                    if move.product_id.type in ['combo', 'consu', 'service']:
                        available_qty = move.product_id.with_context(location=move.location_id.id).qty_available

                        print("=== Internal Transfer Check ===")
                        print("Product:", move.product_id.display_name)
                        print("Available Qty:", available_qty)
                        print("Move Qty:", move.product_uom_qty)

                        if available_qty < move.product_uom_qty:
                            raise UserError(_(
                                "Not enough stock for product '%s' in source location '%s'.\n"
                                "Required: %s %s\n"
                                "Available: %s %s"
                            ) % (
                                move.product_id.display_name,
                                move.location_id.display_name,
                                move.product_uom_qty, move.product_uom.name,
                                available_qty, move.product_uom.name
                            ))

    def button_validate(self):
        """Check stock availability before validation (only once)."""
        for picking in self:
            if picking.picking_type_code in ['internal', 'outgoing']:
                picking._check_stock_availability()
        return super().button_validate()

    # def button_validate(self):
    #     """Override to check stock before validating picking."""
    #     for picking in self:
    #         if picking.picking_type_code in ['internal', 'outgoing']:
    #             # Avoid double check if already done by create/write
    #             picking.with_context(skip_stock_check=True)._check_stock_availability()
    #     return super(StockPicking, self).button_validate()

    # def button_validate(self):
    #     res = super().button_validate()
    #     # Check again at validation
    #     self._check_stock_availability()
    #     return res




