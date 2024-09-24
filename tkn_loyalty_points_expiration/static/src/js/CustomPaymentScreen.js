odoo.define('tkn_loyalty_points_expiration.PaymentScreen', function (require) {
  'use strict';

  const PaymentScreen = require('point_of_sale.PaymentScreen');
  const Registries = require('point_of_sale.Registries');
  const rpc = require('web.rpc');

  const CustomPaymentScreen = PaymentScreen =>
      class extends PaymentScreen {
          async validateOrder(isForceValidate) {
              await super.validateOrder(isForceValidate);

              if (this.currentOrder.is_paid()) {
                  // Recuperamos los datos necesarios de la orden
                  const currentOrder = this.env.pos.get_order();
                  console.log('currentOrder -> ', currentOrder)
                  const partnerId = currentOrder.get_client()?.id;
                  const wonPoints = currentOrder.get_won_points();
                  const spentPoints = currentOrder.get_spent_points();
                  console.log('partnerId -> ', partnerId)

                  if (partnerId && wonPoints !== undefined && spentPoints !== undefined) {
                      // Realizamos una llamada RPC para crear el registro de loyalty.points
                      try {
                          const result = await rpc.query({
                              model: 'loyalty.points',
                              method: 'create',
                              args: [{
                                  partner_id: partnerId,
                                  won_points: wonPoints,
                                  aux_points: wonPoints,
                                  spent_points: spentPoints,
                              }],
                          });

                          console.log('result -> ', result)

                          console.log('Puntos de lealtad guardados exitosamente');
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
