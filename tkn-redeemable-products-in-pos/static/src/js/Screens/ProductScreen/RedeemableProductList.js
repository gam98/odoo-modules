odoo.define('tkn_redeemable_products_in_pos.RedeemableProductList', function (require) {
  'use strict';

  const PosComponent = require('point_of_sale.PosComponent');
  const Registries = require('point_of_sale.Registries');

  class RedeemableProductList extends PosComponent {
    constructor() {
      super(...arguments);
      this.selectProduct = this.selectProduct.bind(this);
  }
    selectProduct(event) {
      this.trigger('product-selected', { product: event.detail.product });
    }
  }

  RedeemableProductList.template = 'RedeemableProductList';

  Registries.Component.add(RedeemableProductList);

  return RedeemableProductList;
});
