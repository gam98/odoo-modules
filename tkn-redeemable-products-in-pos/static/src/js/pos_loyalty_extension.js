odoo.define('tkn_redeemable_products_in_pos.pos_loyalty_extension', function (require) {
  "use strict";

  var models = require('point_of_sale.models');
  var _super_order = models.Order.prototype;
  var utils = require('web.utils');
  var round_pr = utils.round_precision;

  models.Order = models.Order.extend({

    get_won_points: function () {
      if (!this.pos.loyalty || !this.get_client()) {
        return 0;
      }
      var total_points = 0;
      for (var line of this.get_orderlines()) {
        if (line.get_reward()) {  // Reward products are ignored
          continue;
        }

        var line_points = 0;
        this.pos.loyalty.rules.forEach(function (rule) {
          var rule_points = 0
          if (rule.valid_product_ids.find(function (product_id) { return product_id === line.get_product().id })) {
            rule_points += rule.points_quantity * line.get_quantity();
            rule_points += rule.points_currency * line.get_price_with_tax();
          }
          if (Math.abs(rule_points) > Math.abs(line_points))
            line_points = rule_points;
        });

        total_points += line_points;
      }
      total_points += this.get_total_with_tax() * this.pos.loyalty.points;
      return Math.floor(total_points);
    },

    get_spent_points: function () {
      var basePoints = _super_order.get_spent_points.apply(this, arguments);
      if (!this.pos.loyalty || !this.get_client()) {
        return 0;
      } else {
        var points = 0;

        for (var line of this.get_orderlines()) {
          var reward = this.pos.rewardsInMemory?.find((reward) => reward.id === line.product.id && line.price === 0);
          if (reward) {
            points += round_pr(line.get_quantity() * reward.point_cost, 1);
          }
        }

        return basePoints + points;
      }
    },

    async apply_reward(reward) {
      var client = this.get_client();
      var product, product_price, order_total, spendable;
      var crounding;

      if (!client) {
        return;
      } else if (reward.reward_type === 'gift') {
        product = this.pos.db.get_product_by_id(reward.gift_product_id[0]);

        if (!product) {
          return;
        }

        let options = await this._getAddProductOptions(product);
        await this.add_product(product, {
          ...options,
          price: 0,
          quantity: 1,
          merge: false,
          extras: { reward_id: reward.id, price_manually_set: true, point_cost: reward.point_cost },
        });

      } else if (reward.reward_type === 'discount') {

        crounding = this.pos.currency.rounding;
        spendable = this.get_spendable_points();
        order_total = this.get_total_with_tax();
        var discount = 0;

        product = this.pos.db.get_product_by_id(reward.discount_product_id[0]);

        if (!product) {
          return;
        }

        if (reward.discount_type === "percentage") {
          if (reward.discount_apply_on === "on_order") {
            discount += round_pr(order_total * (reward.discount_percentage / 100), crounding);
          }

          if (reward.discount_apply_on === "specific_products") {
            for (var prod of reward.discount_specific_product_ids) {
              var specific_products = this.pos.db.get_product_by_id(prod);

              if (!specific_products)
                return;

              for (var line of this.get_orderlines()) {
                if (line.product.id === specific_products.id)
                  discount += round_pr(line.get_price_with_tax() * (reward.discount_percentage / 100), crounding);
              }
            }
          }

          if (reward.discount_apply_on === "cheapest_product") {
            var price;
            for (var line of this.get_orderlines()) {
              if ((!price || price > line.get_unit_price()) && line.product.id !== product.id) {
                discount = round_pr(line.get_price_with_tax() * (reward.discount_percentage / 100), crounding);
                price = line.get_unit_price();
              }
            }
          }
          if (reward.discount_max_amount !== 0 && discount > reward.discount_max_amount)
            discount = reward.discount_max_amount;

          let options = await this._getAddProductOptions(product);
          await this.add_product(product, {
            ...options,
            price: -discount,
            quantity: 1,
            merge: false,
            extras: { reward_id: reward.id, price_manually_set: true },
          });
        }
        if (reward.discount_type == "fixed_amount") {
          let discount_fixed_amount = reward.discount_fixed_amount;
          let point_cost = reward.point_cost;
          let quantity_to_apply = Math.floor(spendable / point_cost);
          let amount_discounted = discount_fixed_amount * quantity_to_apply;

          if (amount_discounted > order_total) {
            quantity_to_apply = Math.floor(order_total / discount_fixed_amount);
          }

          let options = await this._getAddProductOptions(product);
          await this.add_product(product, {
            ...options,
            price: - discount_fixed_amount,
            quantity: quantity_to_apply,
            merge: false,
            extras: { reward_id: reward.id, price_manually_set: true, point_cost: reward.point_cost },
          });

        }
      }
    },

  });
});


