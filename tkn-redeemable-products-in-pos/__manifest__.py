# -*- coding: utf-8 -*-
{
    'name': "Custom POS Loyalty Program",

    'summary': """
       Extends the loyalty program in POS to allow customers to redeem products based on their loyalty points. Includes a custom button in POS that opens a modal with product search, shows points required, and adds the product to the order if sufficient points are available.""",

    'description': """
        This module enhances the loyalty program functionality in Odoo POS by allowing customers to redeem products directly in the POS interface. 
        Key features:
        - Custom button in POS for accessing the loyalty redemption modal.
        - Product search functionality within the modal.
        - Display of loyalty points required to redeem a selected product.
        - Validation to ensure the customer has enough points before adding the product to the order.
    """,

    'author': 'Tinkin Tech Partner',
    'website': 'https://www.tinkin.one',

    'category': 'Point of Sale',
    'version': '0.1',

    'depends': ['base', 'point_of_sale'],

    'data': [],
    
    'license': 'LGPL-3',

    'version': '15.0.x.x',

    'assets': {
       'point_of_sale.assets': [
          'tkn-redeemable-products-in-pos/static/src/css/index.css',
          'tkn-redeemable-products-in-pos/static/src/js/Popups/RedeemableProductsPopup.js',
          'tkn-redeemable-products-in-pos/static/src/js/Screens/ProductScreen/RedeemableProductList.js',
          'tkn-redeemable-products-in-pos/static/src/js/Screens/ProductScreen/RedeemableProductItem.js',
          'tkn-redeemable-products-in-pos/static/src/js/CustomLoyalty.js',
          'tkn-redeemable-products-in-pos/static/src/js/Screens/ProductScreen/RedeemableProductsWidget.js',
          'tkn-redeemable-products-in-pos/static/src/js/Screens/ProductScreen/RedeemableProductsWidgetControlPanel.js',
          'tkn-redeemable-products-in-pos/static/src/js/Widgets/RedeemableCategoryButton.js',
          'tkn-redeemable-products-in-pos/static/src/js/Widgets/RedeemableCategoryBreadcrumb.js',
          'tkn-redeemable-products-in-pos/static/src/js/Widgets/RedeemableHomeCategoryBreadcrumb.js',
          'tkn-redeemable-products-in-pos/static/src/js/Widgets/RedeemableCategorySimpleButton.js',
          'tkn-redeemable-products-in-pos/static/src/js/CustomPointsCounter.js',
          'tkn-redeemable-products-in-pos/static/src/js/ProductScreenLoyaltyPointsValidation.js',
          'tkn-redeemable-products-in-pos/static/src/js/Screens/ProductScreen/CustomOrderline.js',
          'tkn-redeemable-products-in-pos/static/src/js/CustomRewardButton.js',
          'tkn-redeemable-products-in-pos/static/src/js/Popups/CustomRewardButtonPopup.js',
          'tkn-redeemable-products-in-pos/static/src/js/Screens/TicketScreen/TicketScreenValidation.js',
       ],
       'web.assets_qweb': [
          'tkn-redeemable-products-in-pos/static/src/xml/Screens/ProductScreen/RedeemableProductList.xml',
          'tkn-redeemable-products-in-pos/static/src/xml/Screens/ProductScreen/RedeemableProductItem.xml',
          'tkn-redeemable-products-in-pos/static/src/xml/Screens/ProductScreen/RedeemableProductsWidget.xml',
          'tkn-redeemable-products-in-pos/static/src/xml/Screens/ProductScreen/RedeemableProductsWidgetControlPanel.xml',
          'tkn-redeemable-products-in-pos/static/src/xml/Widgets/RedeemableCategoryButton.xml',
          'tkn-redeemable-products-in-pos/static/src/xml/Widgets/RedeemableCategoryBreadcrumb.xml',
          'tkn-redeemable-products-in-pos/static/src/xml/Widgets/RedeemableHomeCategoryBreadcrumb.xml',
          'tkn-redeemable-products-in-pos/static/src/xml/Widgets/RedeemableCategorySimpleButton.xml',
          'tkn-redeemable-products-in-pos/static/src/xml/CustomPointsCounter.xml',
          'tkn-redeemable-products-in-pos/static/src/xml/Screens/ProductScreen/CustomOrderline.xml',
          'tkn-redeemable-products-in-pos/static/src/xml/CustomRewardButton.xml',
          'tkn-redeemable-products-in-pos/static/src/xml/Popups/CustomRewardButtonPopup.xml',
          'tkn-redeemable-products-in-pos/static/src/xml/Popups/RedeemableProductsPopup.xml',
       ],
    }
}

