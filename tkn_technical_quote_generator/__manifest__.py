# -*- coding: utf-8 -*-
{
    'name': "tkn_technical_quote_generator",

    'summary': """
        Generation of PDF Quotation in Ecommerce with differentiated prices for public, technical and referred customers.""",

    'description': """
        This custom module allows you to generate a PDF quotation from the ecommerce, offering three types of prices: retail price, differentiated price for technicians and special price for referred customers. It includes advanced functionality to define and display prices according to the type of customer, providing an optimized experience for the presentation of quotations.
    """,

    'author': 'Tinkin Tech Partner',

    'website': 'https://www.tinkin.one',

    'category': 'Website',

    'version': '0.1',

    'depends': ['website', 'sale', 'website_payment'],
        
    'license': 'LGPL-3',

    'version': '15.0.x.x',

    'data': [
        'views/templates.xml',
        'report/price_for_referred_customer/quotation_report_templates.xml',
        'report/price_for_referred_customer/quotation_report_action.xml',    
        'report/retail_price/quotation_report_action.xml',
        'report/retail_price/quotation_report_templates.xml',
        'report/differentiated_price_for_being_technician/quotation_report_action.xml',
        'report/differentiated_price_for_being_technician/quotation_report_templates.xml',
    ],

    'demo': [],
}
