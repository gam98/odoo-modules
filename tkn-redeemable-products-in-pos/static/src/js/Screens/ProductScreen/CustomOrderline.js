odoo.define('tkn_redeemable_products_in_pos.CustomOrderline', function (require) {
  'use strict';

  const Orderline = require('point_of_sale.Orderline');
  const Registries = require('point_of_sale.Registries');

  const CustomOrderline = Orderline =>

    class CustomOrderline extends Orderline {

      get pointsToWin() {
        let linePoints = 0;

        this.props.line.pos.loyalty.rules.forEach(rule => {
          let rulePoints = 0

          const productExist = rule.valid_product_ids.find(product_id => product_id === this.props.line.product.id);

          if (productExist) {
            rulePoints += rule.points_currency * this.props.line.get_price_with_tax();
          }

          if (Math.abs(rulePoints) > Math.abs(linePoints)) {
            linePoints = rulePoints;
          }
        })

        if(linePoints < 0) {
          return Math.ceil(linePoints);
        } else {
          return Math.floor(linePoints);
        }

      }

      get pointsToSpentInPromotionalReward() {
        const linePoints = this.props.line.pos.loyalty.rewards.find(reward => reward.id === this.props.line.reward_id);

        return linePoints;
      }

    }

  Registries.Component.extend(Orderline, CustomOrderline);

  return CustomOrderline;
});
