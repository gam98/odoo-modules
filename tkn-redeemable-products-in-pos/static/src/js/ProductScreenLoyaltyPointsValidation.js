odoo.define('tkn_redeemable_products_in_pos.ProductScreenLoyaltyPointsValidation', function(require) {
  'use strict';

  const ProductScreen = require('point_of_sale.ProductScreen');
  const Registries = require('point_of_sale.Registries');

  const ProductScreenLoyaltyPointsValidation = ProductScreen => class extends ProductScreen {
      async _onClickPay() {
        const order = this.env.pos.get_order();
        const new_total_points = order.get_new_total_points();

        console.log('new_total_points', new_total_points);

        if (new_total_points < 0) {
            await this.showPopup('ErrorPopup', {
                title: this.env._t('Advertencia'),
                body: this.env._t('No está permitido acumular puntos negativos.'),
            });
            return; 
        }

          super._onClickPay();
      }
  };

  Registries.Component.extend(ProductScreen, ProductScreenLoyaltyPointsValidation);

  return ProductScreen;
});
