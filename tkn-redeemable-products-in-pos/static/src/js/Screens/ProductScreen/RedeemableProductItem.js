odoo.define('point_of_sale.RedeemableProductItem', function (require) {
  'use strict';

  const PosComponent = require('point_of_sale.PosComponent');
  const Registries = require('point_of_sale.Registries');
  const models = require('point_of_sale.models');

  class RedeemableProductItem extends PosComponent {
    
    selectProduct() {
      this.env.bus.trigger('product-selected', { product: this.props.product });
    }

    spaceClickProduct(event) {
      if (event.which === 32) {
        this.trigger('click-product', this.props.product);
      }
    }
    get imageUrl() {
      const product = this.props.product;
      return `/web/image?model=product.product&field=image_128&id=${product.id}&write_date=${product.write_date}&unique=1`;
    }
    get pricelist() {
      const current_order = this.env.pos.get_order();
      if (current_order) {
        return current_order.pricelist;
      }
      return this.env.pos.default_pricelist;
    }
    get price() {
      const formattedUnitPrice = this.env.pos.format_currency(
        this.props.product.get_display_price(this.pricelist, 1),
        'Product Price'
      );
      if (this.props.product.to_weight) {
        return `${formattedUnitPrice}/${this.env.pos.units_by_id[this.props.product.uom_id[0]].name
          }`;
      } else {
        return formattedUnitPrice;
      }
    }
    async onProductInfoClick() {
      const info = await this.env.pos.getProductInfo(this.props.product, 1);
      this.showPopup('ProductInfoPopup', { info: info, product: this.props.product });
    }
  }
  RedeemableProductItem.template = 'RedeemableProductItem';

  Registries.Component.add(RedeemableProductItem);

  return RedeemableProductItem;
});
