odoo.define('tkn_redeemable_products_in_pos.redeemableProductsPopup', function (require) {
  'use strict';

  const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
  const { Gui } = require('point_of_sale.Gui');
  const Registries = require('point_of_sale.Registries');

  class RedeemableProductsPopup extends AbstractAwaitablePopup {

    constructor() {
      super(...arguments);
      this.state = {
        pointsToRedeem: this.props.points,  // Inicialmente todos los puntos disponibles
        products: this.props.products,
        selectedProduct: null,
        percentage: null,
        pointsNeeded: null
      };
      this.onProductSelected = this.onProductSelected.bind(this);

    }

    onProductSelected(event) {
      console.log('evnet!', event);
      this.state.selectedProduct = event.detail.product;
      console.log('selectedProduct!!!', this.state.selectedProduct);
      // Aquí puedes hacer algo con el producto seleccionado, como calcular los puntos necesarios
      this.render();
    }
    onInputChange(event) {
      this.state.percentage = parseFloat(event.target.value) || 0;
      this.updatePointsNeeded();
    }

    updatePointsNeeded() {
      if (this.state.selectedProduct && this.state.percentage > 0) {
        const pointsNeeded = (this.state.selectedProduct.lst_price / this.state.percentage) * 100;
        this.state.pointsNeeded = Math.ceil(pointsNeeded);  // Redondea al entero más cercano
        this.render();  // Asegúrate de que la interfaz de usuario se actualice
      } else {
        this.state.pointsNeeded = null;
        this.render();
      }
    }

    async confirm() {
      let order = this.env.pos.get_order();
      let reward = {
        name: this.state.selectedProduct.display_name,
        point_cost: this.state.pointsNeeded,
        discount_apply_on: 'on_order',
        reward_type: 'gift',
        gift_product_id: [
          this.state.selectedProduct.id,
          this.state.selectedProduct.display_name
        ],
        id: this.state.selectedProduct.id
      };

      // Store the reward in the pos instance
      if (!this.env.pos.rewardsInMemory) {
        this.env.pos.rewardsInMemory = [];
      }
      this.env.pos.rewardsInMemory.push(reward);

      // Apply the reward to the order
      order.apply_reward(reward);

      this.props.resolve({ confirmed: true, payload: {} });
    }
  }

  RedeemableProductsPopup.template = 'RedeemableProductsPopup';

  RedeemableProductsPopup.defaultProps = {
    confirmText: 'Canjear',
    cancelText: 'Cancelar',
  };

  Registries.Component.add(RedeemableProductsPopup);

  return RedeemableProductsPopup;


});
