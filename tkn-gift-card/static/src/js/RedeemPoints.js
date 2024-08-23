odoo.define('tkn_gift_card.redeemPoints', function (require) {
  'use strict';

  const { Gui } = require('point_of_sale.Gui');
  const PosComponent = require('point_of_sale.PosComponent');
  const { useListener } = require('web.custom_hooks');
  const ProductScreen = require('point_of_sale.ProductScreen');
  const Registries = require('point_of_sale.Registries');

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

      const points = client.loyalty_points;

      if (points <= 0) {
        Gui.showPopup('ErrorPopup', {
          title: this.env._t('Puntos insuficientes'),
          body: this.env._t('Este cliente no tiene puntos suficientes para canjear.'),
        });
        return;
      }


      const { confirmed, payload } = await this.showPopup('RedeemPointsPopup', {
        title: this.env._t('Canjear puntos por gift card'),
        client,
        points,
      });

      if (confirmed && payload) {
        const { pointsToRedeem } = payload;
        const giftCardValue = this.calculateGiftCardValue(pointsToRedeem);
        await this.redeemPointsForGiftCard({ points: pointsToRedeem, client, giftCardValue });
      }
    }

    async redeemPointsForGiftCard({ points, client, giftCardValue }) {
      try {
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
      return points / 100;
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
