odoo.define('tkn_loyalty_points_expiration.saveLoyaltyPoints', function (require) {
  "use strict";

  var models = require('point_of_sale.models');
  var _super_order = models.Order.prototype;

  models.Order = models.Order.extend({
    export_as_JSON: function () {
      var json = _super_order.export_as_JSON.apply(this, arguments);
      if (this.pos.loyalty && this.get_client()) {        
        json.loyalty_points_won = this.get_won_points();
        json.loyalty_points_spent = this.get_spent_points();
        json.loyalty_points_total = this.get_new_points();
      }
      console.log({json});  // <-- Verifica el JSON aquí
      return json;
    },
  });

});
