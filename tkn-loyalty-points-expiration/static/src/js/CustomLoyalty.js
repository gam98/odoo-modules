// odoo.define('tkn_loyalty_points_expiration', function (require) {
//   "use strict";

//   var models = require('point_of_sale.models');
//   var _super_order = models.Order.prototype;
//   var utils = require('web.utils');
//   var round_pr = utils.round_precision;
//   var rpc = require('web.rpc');

//   models.Order = models.Order.extend({
//     set_client: function (client) {
//       var old_client = this.get_client();
//       _super_order.set_client.apply(this, arguments);
//       if (client && client !== old_client) {
//         this.load_loyalty_points(client);
//       }
//     },

//     load_loyalty_points: function (client) {
//       var self = this;
//       return rpc.query({
//         model: 'loyalty.points',
//         method: 'get_points_for_partner',
//         args: [client.id],
//       }).then(function (points) {
//         console.log('Points loaded for client', client.id, '->', points);
//         self.loyalty_points = points;
//       }).catch(function (error) {
//         console.error('Error loading loyalty points:', error);
//       });
//     },

//     get_loyalty_points: function () {
//       // return this.loyalty_points || [];
//       return this.loyalty_points || [];
//     },

//     get_spent_points: function () {
//       var client = this.get_client();
//       if (!client) {
//         return 0;
//       }
//       var points = 0;
//       var loyalty_points = this.get_loyalty_points();
//       console.log('loyalty_points ->', loyalty_points);
//       for (var line of this.get_orderlines()) {
//         var reward = line.get_reward();
//         if (reward) {
//           points += round_pr(line.get_quantity() * reward.point_cost, 1);
//         }
//       }
//       return points;
//     },

//     get_new_total_points: function () {
//       if (!this.pos.loyalty || !this.get_client()) {
//         return 0;
//       } else {
//         if (this.state != 'paid') {
//           return round_pr(this.get_client().loyalty_points + this.get_new_points(), 1);
//         }
//         else {
//           return round_pr(this.get_client().loyalty_points, 1);
//         }
//       }
//     },


//   });
// });

