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
            rulePoints += rule.points_currency * this.props.line.price * this.props.line.quantity;
          }
          
          if (Math.abs(rulePoints) > Math.abs(linePoints)) {
            linePoints = rulePoints;
          }
        })

        return Math.floor(linePoints);
      }

      get pointsToSpentInPromotionalReward() {
        const linePoints = this.props.line.pos.loyalty.rewards.find(reward => reward.id === this.props.line.reward_id && this.props.line.price === 0);

        return linePoints;
      }

    }

  Registries.Component.extend(Orderline, CustomOrderline); 

  return CustomOrderline;
});
