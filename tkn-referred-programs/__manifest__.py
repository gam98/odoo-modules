# -*- coding: utf-8 -*-

{
    'name': 'Referred programs Servicat',
    'summary': 'Referred programs Servicat',
    'description': """
       This module updates loyalty points accumulation if the order is completed using some referred coupon.
       If the order has no coupon, the points will add to the client, but if the order has any referred coupon, 
       the points will be added to the owner of the coupon program.
    """,
    'author': 'Tinkin Tech Partner',
    'website': 'https://www.tinkin.one',
    'version': '15.0.x.x',
    'depends': [
        'base',
        'point_of_sale',
        'ek_pos_retail_with_sap',
        'tkn_loyalty_points_expiration'
    ],
    'data': [],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}
