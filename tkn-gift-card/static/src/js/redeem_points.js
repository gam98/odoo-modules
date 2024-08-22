odoo.define('tkn_gift_card.redeem_points', function (require) {
  'use strict';

  const { Gui } = require('point_of_sale.Gui');
  const PosComponent = require('point_of_sale.PosComponent');
  const { useListener } = require('web.custom_hooks');
  const ProductScreen = require('point_of_sale.ProductScreen');
  const Registries = require('point_of_sale.Registries');
  const rpc = require('web.rpc');

  class RedeemPoints extends PosComponent {

    constructor() {
      super(...arguments);
      useListener('click', this.onClick);
    }

    async onClick() {
      const client = this.env.pos.get_client();

      if (!client) {
        Gui.showPopup('ErrorPopup', {
          title: this.env._t('Cliente no encontrado'),
          body: this.env._t('Por favor, seleccione un cliente antes de continuar.'),
        });
        return;
      }

      console.log('Client:', client);

      const points = client.loyalty_points;
      if (points <= 0) {
        Gui.showPopup('ErrorPopup', {
          title: this.env._t('Puntos insuficientes'),
          body: this.env._t('Este cliente no tiene puntos suficientes para canjear.'),
        });
        return;
      }

      const giftCardValue = this.calculateGiftCardValue(points);

      const { confirmed } = await Gui.showPopup('ConfirmPopup', {
        title: this.env._t('Canjear puntos por gift card'),
        body: this.env._t(`Tienes ${points} puntos. Esto equivale a una gift card de ${giftCardValue} unidades monetarias. ¿Deseas canjear?`),
        cancelText: this.env._t('Cancelar'),
        confirmText: this.env._t('Canjear'),
        inputType: 'number',  // Aquí especificas que el tipo de entrada es un número
        value: 1,  // Valor inicial del campo
        confirm: (value) => {
          if (value !== null) {
            console.log('Cantidad ingresada:', value);
            // Aquí puedes agregar la lógica para manejar el valor ingresado
          }
        },
      });

      if (confirmed) {
        await this.redeemPointsForGiftCard({ points, client, giftCardValue });
      }

    }

    async redeemPointsForGiftCard({ points, client, giftCardValue }) {
      try {
        // Crear la gift card en el backend
        console.log('Gift Card Value:', giftCardValue);
        console.log('Client:', client);
        const giftCard = await rpc.query({
          model: 'loyalty.card',
          method: 'create',
          args: [{
            client_id: client.id,
            value: giftCardValue,
          }],
        });

        console.log('Gift Card:', giftCard);

        // Actualizar puntos del cliente
        // await this.rpc({
        //   model: 'pos.order',
        //   method: 'write',
        //   args: [[client.loyalty_points_id], { 'points': client.loyalty_points - points }],
        // });

        Gui.showPopup('ConfirmPopup', {
          title: this.env._t('Gift Card Creada'),
          body: this.env._t(`Se ha creado una gift card de valor ${giftCardValue} para el cliente ${client.name}.`),
        });

      } catch (error) {
        Gui.showPopup('ErrorPopup', {
          title: this.env._t('Error'),
          body: this.env._t('Hubo un error al intentar crear la gift card. Por favor, intente nuevamente.'),
        });
        console.error('Error al canjear puntos por gift card:', error);
      }
    }


    calculateGiftCardValue(points) {
      // Aquí implementas la lógica para convertir puntos en valor de gift card
      return points / 100; // Ejemplo: 1 punto = 0.1 de valor
    }

  }

  RedeemPoints.template = 'RedeemPoints';

  ProductScreen.addControlButton({
    component: RedeemPoints,
    condition: function () {
      return this.env.pos;
    },
  });

  Registries.Component.add(RedeemPoints);

  return RedeemPoints;
});
