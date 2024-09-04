odoo.define('tkn_redeemable_products_in_pos.pos_loyalty_extension', function (require) {
  "use strict";

  var models = require('point_of_sale.models');
  var _super_order = models.Order.prototype;
  var utils = require('web.utils');
  var round_pr = utils.round_precision;

  models.Order = models.Order.extend({

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

  });
});
