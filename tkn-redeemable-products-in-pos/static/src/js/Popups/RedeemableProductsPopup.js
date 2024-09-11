odoo.define('tkn_redeemable_products_in_pos.redeemableProductsPopup', function (require) {
  'use strict';

  const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
  const Registries = require('point_of_sale.Registries');

  class RedeemableProductsPopup extends AbstractAwaitablePopup {

    constructor() {
      super(...arguments);
      this.state = {
        pointsToRedeem: this.env.pos.get('clientLoyaltyPoints'),
        selectedProduct: null,
        percentage: 2.5,
        pointsNeeded: null,
        priceWithTaxes: null
      };
    }

    _onProductSelected(event) {
      this.state.selectedProduct = event.product;
      this.updatePointsNeeded();
      this.render();
    }

    mounted() {
      this.env.bus.on('product-selected', this, this._onProductSelected);
    }

    willUnmount() {
      this.env.bus.off('product-selected', this);
    }

    get isAcceptButtonDisabled() {
      return !this.state.selectedProduct ||
        this.state.pointsNeeded > this.props.points ||
        !this.state.percentage;
    }

    onInputChange(event) {
      this.state.percentage = parseFloat(event.target.value) || 0;
      this.updatePointsNeeded();
    }

    updatePointsNeeded() {
      if (this.state.selectedProduct && this.state.percentage > 0) {

        const { taxes } = this.state.selectedProduct.pos;
        const { taxes_id, lst_price } = this.state.selectedProduct;

        let totalTaxes = 0;
        for (const taxId of taxes_id) {
          totalTaxes += taxes[taxId].amount;
        }

        const priceWithTaxes = (lst_price + (lst_price * totalTaxes / 100)).toFixed(2);
        this.state.priceWithTaxes = priceWithTaxes;
        const pointsNeeded = (priceWithTaxes / this.state.percentage) * 100;
        this.state.pointsNeeded = Math.ceil(pointsNeeded);
        this.render();
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
        id: this.state.selectedProduct.id,
        is_custom_reward: true
      };

      order.apply_reward(reward);

      const currentLoyaltyPoints = this.env.pos.get('clientLoyaltyPoints');

      this.env.pos.set('clientLoyaltyPoints', currentLoyaltyPoints - this.state.pointsNeeded);

      this.trigger('close-popup');
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
