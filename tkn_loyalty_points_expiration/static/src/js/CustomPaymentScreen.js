odoo.define('tkn_loyalty_points_expiration.PaymentScreen', function (require) {
  'use strict';

  const PaymentScreen = require('point_of_sale.PaymentScreen');
  const Registries = require('point_of_sale.Registries');
  const rpc = require('web.rpc');

  const CustomPaymentScreen = PaymentScreen =>
    class extends PaymentScreen {

      isTechnical() {
        const client = this.env.pos.get('client') || this.env.pos.get_client();
        return client.classification_id[1] === 'TECNICO';
      }

      async validateOrder(isForceValidate) {
        await super.validateOrder(isForceValidate);

        if (this.currentOrder.is_paid()) {

          const { name } = this.currentOrder
          const currentOrder = this.env.pos.get_order();
          const partnerId = currentOrder.get_client()?.id;
          const wonPoints = currentOrder.get_won_points();
          const spentPoints = currentOrder.get_spent_points();

          if (partnerId && this.isTechnical() && wonPoints !== undefined && spentPoints !== undefined) {
            try {
              await rpc.query({
                model: 'loyalty.points',
                method: 'create',
                args: [{
                  partner_id: partnerId,
                  won_points: wonPoints,
                  aux_points: wonPoints,
                  spent_points: spentPoints,
                  order_name: name
                }],
              });

            } catch (error) {
              console.error('Error al guardar los puntos de lealtad:', error);
            }
          }
        } 

      }
    };

  Registries.Component.extend(PaymentScreen, CustomPaymentScreen);

  return CustomPaymentScreen;
});
