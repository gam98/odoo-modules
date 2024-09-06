odoo.define('tkn_redeemable_products_in_pos.ProductScreenLoyaltyPointsValidation', function (require) {
  'use strict';

  const ProductScreen = require('point_of_sale.ProductScreen');
  const Registries = require('point_of_sale.Registries');

  const ProductScreenLoyaltyPointsValidation = ProductScreen => class extends ProductScreen {
    async _onClickPay() {
      const order = this.env.pos.get_order();
      const new_total_points = order.get_new_total_points();

      if (new_total_points < 0) {
        await this.showPopup('ErrorPopup', {
          title: this.env._t('Advertencia'),
          body: this.env._t('No está permitido acumular puntos negativos.'),
        });
        return;
      }

      let purchaseSummary = {
        rewardSpending: 0,
        regularSpending: 0
      }

      order.orderlines.models.forEach(line => {
        if (line.reward_id) {
          purchaseSummary['rewardSpending'] += line.product.lst_price;
        } else {
          purchaseSummary['regularSpending'] += line.product.lst_price;
        }
      })

      const totalInvoice = purchaseSummary['regularSpending'] + purchaseSummary['rewardSpending'];

      const maxPointsValueAllowed = totalInvoice * 0.7;

      if (purchaseSummary['rewardSpending'] > maxPointsValueAllowed) {
        await this.showPopup('ErrorPopup', {
          title: this.env._t('Límite de canje de puntos superado'),
          body: this.env._t('No puedes canjear más del 70% del valor de tu factura en puntos de recompensa. Por favor, ajusta tu selección.'),
        });
        return;
      }

      super._onClickPay();
    }
  };

  Registries.Component.extend(ProductScreen, ProductScreenLoyaltyPointsValidation);

  return ProductScreen;
});
