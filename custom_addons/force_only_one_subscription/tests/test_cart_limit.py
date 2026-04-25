from odoo.tests import tagged

from odoo.addons.website.tools import MockRequest
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale.tests.common import WebsiteSaleCommon


@tagged("post_install", "-at_install")
class TestCartLimit(WebsiteSaleCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website_sale_controller = WebsiteSale()
        cls.replacement_product = cls._create_product(
            name="Replacement Product",
            list_price=125.0,
        )

    def test_latest_added_product_replaces_existing_cart_lines(self):
        website = self.website.with_user(self.public_user)
        public_env = self.env(user=self.public_user.id)

        with MockRequest(public_env, website=website):
            self.website_sale_controller.cart_update_json(product_id=self.product.id, add_qty=3)
            sale_order = website.sale_get_order()
            self.assertEqual(len(sale_order.website_order_line), 1)
            self.assertEqual(sale_order.website_order_line.product_id, self.product)
            self.assertEqual(sale_order.website_order_line.product_uom_qty, 1)

            self.website_sale_controller.cart_update_json(
                product_id=self.replacement_product.id,
                add_qty=1,
            )
            self.assertEqual(len(sale_order.website_order_line), 1)
            self.assertEqual(
                sale_order.website_order_line.product_id,
                self.replacement_product,
            )
            self.assertEqual(sale_order.website_order_line.product_uom_qty, 1)

    def test_adding_same_product_again_keeps_single_quantity(self):
        website = self.website.with_user(self.public_user)
        public_env = self.env(user=self.public_user.id)

        with MockRequest(public_env, website=website):
            self.website_sale_controller.cart_update_json(product_id=self.product.id, add_qty=1)
            sale_order = website.sale_get_order()

            self.website_sale_controller.cart_update_json(product_id=self.product.id, add_qty=5)
            self.assertEqual(len(sale_order.website_order_line), 1)
            self.assertEqual(sale_order.website_order_line.product_id, self.product)
            self.assertEqual(sale_order.website_order_line.product_uom_qty, 1)
