# -*- coding: utf-8 -*-
{
    'name': "tkn_technical_quote_generator",

    'summary': """
        Saaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa""",

    'description': """
        aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['website', 'sale', 'website_payment', 'website_mail', 'portal_rating', 'digest'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'report/quotation_report.xml',
        'views/report_sale_order_templates.xml',  # Incluir la plantilla
        'views/report_sale_order_action.xml',     # Incluir la acción del reporte
        'security/ir.model.access.csv',
    ],
    'demo': [],
    'assets': {
      'website_sale.assets': [
        'tkn-technical_quote_generator/static/src/css/index.css',
        'tkn_technical_quote_generator/static/src/js/TechnicalQuoteGeneratorPopup.js',
        'tkn_technical_quote_generator/static/src/js/TechnicalQuoteGeneratorButton.js',
        'tkn_technical_quote_generator/static/src/js/QuoteModal.js',
      ],
      'web.assets_qweb': [
        'tkn_technical_quote_generator/static/src/xml/TechnicalQuoteGeneratorButton.xml',
        'tkn_technical_quote_generator/static/src/xml/TechnicalQuoteGeneratorPopup.xml',
      ]
    }
}
