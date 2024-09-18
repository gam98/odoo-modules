odoo.define('tkn_redeemable_products_in_pos', function (require) {
  "use strict";

  var models = require('point_of_sale.models');
  var _super_order = models.Order.prototype;
  var utils = require('web.utils');
  var round_pr = utils.round_precision;

  models.load_fields('res.partner', 'points');

  models.Order = models.Order.extend({

    get_spent_points: function () {
      console.log('this.get_client ->', this.get_client());
      if (!this.pos.loyalty || !this.get_client()) {
        return 0;
      } else {
        var points = 0;

        for (var line of this.get_orderlines()) {
          var reward = line.get_reward();
          if (reward) {
            points += round_pr(line.get_quantity() * reward.point_cost, 1);
          }
        }
        return points;
      }
    },
  });
});

