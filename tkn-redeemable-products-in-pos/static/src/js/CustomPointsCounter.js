odoo.define('tkn_redeemable_products_in_pos.CustomPointsCounter', function (require) {
  'use strict';

  const PointsCounter = require('pos_loyalty.PointsCounter');
  const Registries = require('point_of_sale.Registries');
  const utils = require('web.utils');

  const round_pr = utils.round_precision;

  const PointsCounterCustom = PointsCounter =>
    class extends PointsCounter {

      get isTechnical() {
        const client = this.env.pos.get('client') || this.env.pos.get_client();
        return client.classification_id[1] === 'TECNICO';
      }
      
      get_points_total() {
        const spentPoints = super.get_points_spent();
        const totalPoints = this.env.pos.get_client().loyalty_points - spentPoints;
        this.env.pos.set('clientLoyaltyPoints', totalPoints);
        return round_pr(totalPoints, this.env.pos.loyalty.rounding);
      }

    };

  Registries.Component.extend(PointsCounter, PointsCounterCustom);

  return PointsCounterCustom;
});


