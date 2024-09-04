odoo.define('tkn_redeemable_products_in_pos.RedeemableProducts', function (require) {
  'use strict';

  const { Gui } = require('point_of_sale.Gui');
  const PosComponent = require('point_of_sale.PosComponent');
  const { useListener } = require('web.custom_hooks');
  const ProductScreen = require('point_of_sale.ProductScreen');
  const Registries = require('point_of_sale.Registries');

  class RedeemableProducts extends PosComponent {
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
      
      if (!this.env.pos.clientLoyaltyPoints) {
        this.env.pos.clientLoyaltyPoints = client.loyalty_points;
      }

      const points = this.env.pos.clientLoyaltyPoints;

      if (points <= 0) {
        Gui.showPopup('ErrorPopup', {
          title: this.env._t('Puntos insuficientes'),
          body: this.env._t('Este cliente no tiene puntos suficientes para canjear puntos por productos.'),
        });
        return;
      }

      const { confirmed, payload } = await this.showPopup('RedeemableProductsPopup', {
        title: this.env._t('Canjear productos por puntos'),
        client,
        points,
      });

      if (confirmed ) {
        this.trigger('close-popup');
      }

    }

  }

  RedeemableProducts.template = 'RedeemableProducts';

  ProductScreen.addControlButton({
    component: RedeemableProducts,
    condition: function () {
      return this.env.pos;
    },
  });

  Registries.Component.add(RedeemableProducts);

  return RedeemableProducts;
});
