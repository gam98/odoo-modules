# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Whatsapp Notification for Loyalty Program',
    'summary': 'Sends notifications via WhatsApp to customers regarding their loyalty points obtained and redeemed after making a purchase.',
    'description': """
        This module integrates with the WhatsApp API to send notifications to customers about their loyalty points. 
        It informs them about points obtained and redeemed through their purchases in the loyalty program.
    """,
    'author': 'Tinkin Tech Partner',
    'website': 'https://www.tinkin.one',
    'version': '15.0.x.x',
    'depends': [
        'base',
        'point_of_sale',
        'tkn-redeemable-products-in-pos',
        'tkn-referred-programs',
    ],
    'data': [],
     'assets': {
        'point_of_sale.assets': [
            'tkn-whatsapp-notification/static/src/js/send_whatsapp.js',  # Ruta a tu archivo JS
        ],
    },
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}
