{
    "name": "Neuroworx Website Single Product Cart",
    "summary": "Ensures only one product can exist in the website cart at any time.",
    "description": """
Neuroworx module for Odoo 18 that enforces a single-product checkout flow.

When a customer adds a product to the cart, any existing product in the cart
will be automatically removed and replaced with the newly selected product.

This is useful for businesses that sell:
- subscription packages
- service packages
- tender access plans
- membership plans
- digital products with single selection requirement

Key Features:
- Guarantees only one product in cart
- Prevents mixed package checkout
- Simplifies pricing logic
- Works seamlessly with Odoo website_sale
- Lightweight and easy to maintain
- Designed for Neuroworx subscription-based solutions

Use Case Example:
Tender subscription plans (3 months, 6 months, yearly) where customers
must choose only one active plan per purchase.
""",
    "author": "Neuroworx",
    "website": "https://neuroworx.com",
    "version": "19.0.1.0.0",
    "category": "Website/eCommerce",
    "depends": ["website_sale"],
    "data": [],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
