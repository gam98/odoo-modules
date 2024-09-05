# -*- coding: utf-8 -*-
{
    'name': "tkn-redeemable-products-in-pos",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'point_of_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
       'point_of_sale.assets': [
          'tkn-redeemable-products-in-pos/static/src/css/popup.css',
          'tkn-redeemable-products-in-pos/static/src/js/RedeemableProducts.js',
          'tkn-redeemable-products-in-pos/static/src/js/RedeemableProductsPopup.js',
          'tkn-redeemable-products-in-pos/static/src/js/RedeemableProductList.js',
          'tkn-redeemable-products-in-pos/static/src/js/RedeemableProductItem.js',
          'tkn-redeemable-products-in-pos/static/src/js/pos_loyalty_extension.js',
          'tkn-redeemable-products-in-pos/static/src/js/RedeemableProductsWidget.js',
          'tkn-redeemable-products-in-pos/static/src/js/RedeemableProductsWidgetControlPanel.js',
          'tkn-redeemable-products-in-pos/static/src/js/Widgets/RedeemableCategoryButton.js',
          'tkn-redeemable-products-in-pos/static/src/js/Widgets/RedeemableCategoryBreadcrumb.js',
          'tkn-redeemable-products-in-pos/static/src/js/Widgets/RedeemableHomeCategoryBreadcrumb.js',
          'tkn-redeemable-products-in-pos/static/src/js/Widgets/RedeemableCategorySimpleButton.js',
          'tkn-redeemable-products-in-pos/static/src/js/CustomPointsCounter.js',
          'tkn-redeemable-products-in-pos/static/src/js/ProductScreenLoyaltyPointsValidation.js',          
       ],
       'web.assets_qweb': [
          'tkn-redeemable-products-in-pos/static/src/xml/RedeemableProducts.xml',
          'tkn-redeemable-products-in-pos/static/src/xml/RedeemableProductList.xml',
          'tkn-redeemable-products-in-pos/static/src/xml/RedeemableProductItem.xml',
          'tkn-redeemable-products-in-pos/static/src/xml/RedeemableProductsWidget.xml',
          'tkn-redeemable-products-in-pos/static/src/xml/RedeemableProductsWidgetControlPanel.xml',
          'tkn-redeemable-products-in-pos/static/src/xml/Widgets/RedeemableCategoryButton.xml',
          'tkn-redeemable-products-in-pos/static/src/xml/Widgets/RedeemableCategoryBreadcrumb.xml',
          'tkn-redeemable-products-in-pos/static/src/xml/Widgets/RedeemableHomeCategoryBreadcrumb.xml',
          'tkn-redeemable-products-in-pos/static/src/xml/Widgets/RedeemableCategorySimpleButton.xml',
          'tkn-redeemable-products-in-pos/static/src/xml/CustomPointsCounter.xml',
          'tkn-redeemable-products-in-pos/static/src/xml/CustomOrderline.xml',
       ],
    }
}

