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
      this.state = {
        points: 0,
      };
      this.env.pos.on('change:clientLoyaltyPoints', this.updatePoints, this);
    }

    mounted() {
      console.log('mounted!');
      // this.env.pos.set('clientLoyaltyPoints', 0);
    }

    willUnmount() {
      console.log('willUnmount!');
      this.env.pos.off('change:clientLoyaltyPoints', this.updatePoints, this);
      this.env.pos.set('clientLoyaltyPoints', 0);
    }

    updatePoints() {
      const currentLoyaltyPoints = this.env.pos.get('clientLoyaltyPoints');

      if (!currentLoyaltyPoints) {
        const client = this.env.pos.get_client();
        this.state.points = client.loyalty_points;
        this.env.pos.set('clientLoyaltyPoints', client.loyalty_points);
      } else {
        this.state.points = currentLoyaltyPoints;
      }
    }

    async onClick() {
      const orders = this.env.pos.get_order().get_orderlines();
      
      const hasNonRedeemableProducts = orders.some(order => order.reward_id === undefined)

      if(!hasNonRedeemableProducts) {
        Gui.showPopup('ErrorPopup', {
          title: this.env._t('Orden requerida para canje'),
          body: this.env._t('Debe tener al menos un producto en la orden para poder canjear puntos. No es posible canjear puntos sin una orden activa que incluya otros productos.'),
        })
        return;
      }

      const client = this.env.pos.get_client();

      if (!client) {
        Gui.showPopup('ErrorPopup', {
          title: this.env._t('Cliente no encontrado'),
          body: this.env._t('Por favor, seleccione un cliente antes de continuar.'),
        });
        return;
      }

      if (client.loyalty_points <= 0) {
        Gui.showPopup('ErrorPopup', {
          title: this.env._t('Puntos insuficientes'),
          body: this.env._t('Este cliente no tiene puntos suficientes para canjear puntos por productos.'),
        });
        return;
      }

      this.updatePoints();

      const points = this.state.points;

      const { confirmed, payload } = await this.showPopup('RedeemableProductsPopup', {
        title: this.env._t('Canjear productos por puntos'),
        client,
        points,
      });

      if (confirmed) {
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


