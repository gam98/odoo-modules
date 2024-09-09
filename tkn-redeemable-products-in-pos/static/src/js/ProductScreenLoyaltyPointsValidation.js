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
        regularSpending: 0,
        giftCardSpending: 0,
      };

      order.orderlines.models.forEach(line => {
        if (line.reward_id) {
          const isGiftCard = line.product.lst_price === 0 && line.is_gift_card;
          if (isGiftCard) {
            const discount = (line.point_cost / 100) * line.quantity;
            purchaseSummary['giftCardSpending'] += discount;
          } else {
            purchaseSummary['rewardSpending'] += line.product.lst_price * line.quantity;
          }
        } else {
          purchaseSummary['regularSpending'] += line.product.lst_price * line.quantity;
        }
      });


      const maxRedeemableAmount = purchaseSummary['regularSpending'] * 0.7;

      const totalSpendingInRewards = purchaseSummary['rewardSpending'] + purchaseSummary['giftCardSpending'];

      console.log(purchaseSummary)

      if (totalSpendingInRewards > maxRedeemableAmount) {
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
