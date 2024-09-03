# -*- coding: utf-8 -*-
{
    'name': "tkn-refund-points",
    'summary': """
        Functionality that refund points when an order is returned and has loyalty points associtated
        """,
    'description': """
        When an order is refunded, any loyalty points gained from 
    that purchase are also revoked. This means that the points earned through
    the refunded transaction will be deducted from the customer's loyalty
    points balance.
    """,
    'author': "Tinkin Tech Partner",
    'website': "http://www.tinkin.one",
    'category': 'Uncategorized',
    'version': '15.0.x.x',
    'depends': ['pos_loyalty', 'sale'],
    'data': [
        'views/views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}
