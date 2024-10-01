# -*- coding: utf-8 -*-

{
    'name': "Odoo and Mercately Integration",
    'summary': """
        Mercately and Odoo's data client sincronization
    """,
    'description': """
        This module updates client's data in Mercately account. It is neccesary to provide 
        system parameters such as api-key of the account and the url from Mercately
    """,
    'author': 'Tinkin Tech Partner',
    'website': 'https://www.tinkin.one',
    'version': '15.0.x.x',
    'depends': ['base', 'tkn_loyalty_points_expiration', 'tkn-referred-programs' ],
    'data': [
        'views/views.xml',
        'views/templates.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'tkn-mercately-integration/static/src/js/update_mercately_data.js',
        ],
    },
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}
