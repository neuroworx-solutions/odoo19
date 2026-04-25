from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @staticmethod
    def _get_requested_cart_quantity(quantity, fallback=0):
        # Website cart values can arrive as strings. Normalize them once so the
        # replacement rule below can make a simple numeric decision.
        if quantity in (None, False, ""):
            return 0
        try:
            return int(quantity)
        except (TypeError, ValueError):
            return fallback

    def _cart_update(self, product_id, line_id=None, add_qty=0, set_qty=0, **kwargs):
        """Keep only the latest website cart product and clamp its quantity to 1."""
        self.ensure_one()

        # Odoo may call _cart_update with either add_qty or set_qty depending on
        # the UI action. We treat any positive request as "make this product the
        # only product in the cart".
        parsed_add_qty = self._get_requested_cart_quantity(
            add_qty,
            fallback=1 if add_qty not in (None, False, "") else 0,
        )
        parsed_set_qty = self._get_requested_cart_quantity(set_qty)

        if parsed_set_qty > 0 or parsed_add_qty > 0:
            # If the same product is already in the cart, keep that line and
            # remove every other visible website cart line.
            target_line = self._cart_find_product_line(
                product_id,
                line_id=line_id,
                **kwargs,
            )[:1]
            lines_to_remove = self.website_order_line - target_line
            if lines_to_remove:
                lines_to_remove.unlink()

            # After cleaning the cart, always force the final quantity to 1 no
            # matter what the user requested from the storefront.
            add_qty = 0
            set_qty = 1

        return super()._cart_update(
            product_id,
            line_id=line_id,
            add_qty=add_qty,
            set_qty=set_qty,
            **kwargs,
        )
