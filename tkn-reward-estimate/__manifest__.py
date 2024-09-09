# -*- coding: utf-8 -*-
{
    'name': "Custom Loyalty Reward Program",

    'summary': 'Extension for the loyalty reward module to calculate promotional and additional points',
    'description': """
        This module extends the functionality of the loyalty reward module to:
        - Calculate points based on a percentage and cost price.
        - Add a method to add points either manually or automatically.
        - Display cost price only for promotional products.
        - Modify the form view to adjust the visibility and calculation of points.
    """,

    'author': 'Tinkin Tech Partner',
    'website': 'https://www.tinkin.one',

    'category': 'Point of Sale',

    'data': [],
    
    'license': 'LGPL-3',

    'version': '15.0.x.x',

    'depends': ['base', 'pos_loyalty'],

    'data': [
        'views/views.xml',
    ],

    'demo': [],
}
