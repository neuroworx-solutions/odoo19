from odoo import models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _is_add_to_cart_allowed(self):
        return False