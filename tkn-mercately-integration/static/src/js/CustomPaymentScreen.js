odoo.define('tkn_loyalty_points_expiration.PaymentScreen', function (require) {
    'use strict';
  
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    const rpc = require('web.rpc');
  
    const CustomPaymentScreen = PaymentScreen =>
        class extends PaymentScreen {
            async validateOrder(isForceValidate) {
                await super.validateOrder(isForceValidate);
                
                
            }
        };
  
    Registries.Component.extend(PaymentScreen, CustomPaymentScreen);
  
    return CustomPaymentScreen;
  });
  