# -*- coding: utf-8 -*-
{
    'name': 'Product Dimensions',
    'summary': 'Product Dimensions',
    'version': '12.0',
    'description': """
Product Dimentions
====================================================
- enable 'dimension in orderline' from UOM form
- in purchase select product template, the length is fetched from the product (in variants tab)
- enter the width and height, and click confirm. The variants are created.
        """,
    'category': 'Sale',
    'author': 'SimplitME',
    'website': 'http://simplit.me/',
    'support': "",
    'depends': [
        'sale',
        'purchase',
    ],
    'data': [
        #'security/ir.model.access.csv',
        'data/attributes.xml',
        'views/views.xml',
        'views/sale_report.xml',
    ],
    'installable': True,
    'application': False,
}
