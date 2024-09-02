# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Whatsapp Notification for Loyalty Program',
    'summary': 'Sends notifications via WhatsApp to customers regarding their loyalty points obtained and redeemed after making a purchase.',
    'description': """
        This module integrates with the WhatsApp API to send notifications to customers about their loyalty points. 
        It informs them about points obtained and redeemed through their purchases in the loyalty program.
    """,
    'author': 'Your Name or Company',
    'website': 'https://www.yourwebsite.com',
    'version': '1.0',
    'depends': [
        'base',
        'point_of_sale',
    ],
    'data': [
    ],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
    'images': [
        'static/description/whatsapp_notification_screenshot.png',
    ],
}
