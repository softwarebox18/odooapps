# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Product Specific Promotion Discounts',
    'summary': """In Odoo 15, there's a problem with the standard promotions feature: you can't apply discounts to just some of the products in an order. This means if you want to give a discount on only a couple of items in a customer's order, you're out of luck. This makes it hard to target promotions to specific products, which can be really useful for boosting sales.""",
    'sequence': -100,
    'version': '15.0.1.0.0',
    'category': 'Sale',
    'author': 'Mudassir Hassan',
    'website': 'http://mudassirh45@gmail.com',
    'module_type': 'industries',
    'price': '35.0',
    'currency': 'USD',
    'depends': ['base','sale', 'sale_coupon'],
    'data': [
        'security/ir.model.access.csv',
        'views/menus.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    'images': ['static/description/main.png'],
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
