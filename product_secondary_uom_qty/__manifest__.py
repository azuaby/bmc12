# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today  Technaureus Info Solutions(<http://www.technaureus.com/>).
{
    "name": "Product Secondary UOM Qty",
    "category": 'Sales',
    "summary": """
        Qty on hand in secondary UOM. 
    """,
    "sequence": 1,
    "author": "Technaureus Info Solutions",
    "website": "http://www.technaureus.com/",
    "version": '1.0',
    'price': 20,
    'currency': 'EUR',
    'license': 'Other proprietary',
    "depends": ['stock','sale','base','purchase'],
    "data": [
        'views/product_view.xml',
    ],
    'qweb': [],
    'images': ['images/uom_screenshot.png'],
    "installable": True,
    "application": True,
    "auto_install": False,
}
