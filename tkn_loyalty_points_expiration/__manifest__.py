# -*- coding: utf-8 -*-
{
    'name': "Loyalty Points Expiration",

    'summary': 'Automatic expiration of loyalty points after 6 months',

    'description': """
        This module for Odoo manages the automatic expiration of loyalty points accumulated by customers. According to company rules, points are valid for 6 months from the date of issuance. Once this period has passed, the points are automatically removed, preventing further use. The module ensures better management of the loyalty program by maintaining up-to-date point balances.
    """,

    'author': 'Tinkin Tech Partner',

    'website': 'https://www.tinkin.one',

    'category': 'Sales',

    'license': 'LGPL-3',

    'version': '15.0.x.x',

    'depends': ['base', 'point_of_sale', 'pos_loyalty'],

    'data': [
        'security/ir.model.access.csv',
    ],

    'demo': [],

}
