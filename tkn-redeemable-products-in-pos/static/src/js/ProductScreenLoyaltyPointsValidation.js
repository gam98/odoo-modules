odoo.define('tkn_redeemable_products_in_pos.ProductScreenLoyaltyPointsValidation', function (require) {
  'use strict';

  const ProductScreen = require('point_of_sale.ProductScreen');
  const Registries = require('point_of_sale.Registries');

  const ProductScreenLoyaltyPointsValidation = ProductScreen => class extends ProductScreen {

    priceWithTaxes(line) {
      const { taxes } = line.pos;
      const { lst_price, taxes_id } = line.product;

      let totalTaxes = 0;
      for (const taxId of taxes_id) {
        totalTaxes += taxes[taxId].amount;
      }

      const priceWithTaxes = (lst_price + (lst_price * totalTaxes / 100)).toFixed(2);

      return priceWithTaxes;
    }

    async _onClickPay() {

      const order = this.env.pos.get_order();
      const new_total_points = order.get_new_total_points();

      const ZERO_LOYALTY_POINTS = 0;

      if (new_total_points < ZERO_LOYALTY_POINTS) {
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
        refundSpending: 0,
      };

      order.orderlines.models.forEach(line => {
        if (line.reward_id) {
          const isGiftCard = line.product.lst_price === 0 && line.is_gift_card;
          if (isGiftCard) {
            const discount = (line.point_cost / 100) * line.quantity;
            purchaseSummary['giftCardSpending'] += discount;
          } else {
            purchaseSummary['rewardSpending'] += this.priceWithTaxes(line) * line.quantity;
          }
        } else if (line.hasOwnProperty('refunded_orderline_id') && line['refunded_orderline_id'] !== undefined) {
          purchaseSummary['refundSpending'] += line.get_price_with_tax();
        } else {
          purchaseSummary['regularSpending'] += line.get_price_with_tax();
        }
      });

      const MINIMUM_REQUIRED_EXPENSE = 1;
      const hasRewardSpending = purchaseSummary['rewardSpending'] > 0;

      if (hasRewardSpending && purchaseSummary['rewardSpending'] < MINIMUM_REQUIRED_EXPENSE) {
        await this.showPopup('ErrorPopup', {
          title: this.env._t('Condiciones para canjear puntos'),
          body: this.env._t('No hay límite mínimo de puntos para canje. Sin embargo, no se puede canjear puntos con un valor inferior a $1.'),
        });
        return;
      }

      const MAX_REDEEMABLE_POINTS_PERCENT = 0.7;

      const maxRedeemableAmount = purchaseSummary['regularSpending'] * MAX_REDEEMABLE_POINTS_PERCENT;

      const totalSpendingInRewards = purchaseSummary['rewardSpending'] + purchaseSummary['giftCardSpending'];

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
