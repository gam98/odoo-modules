odoo.define('tkn_redeemable_products_in_pos.CustomOrderReceipt', function (require) {
  'use strict';

  const OrderReceipt = require('point_of_sale.OrderReceipt');
  const Registries = require('point_of_sale.Registries');

  const CustomOrderReceipt = OrderReceipt =>
    class extends OrderReceipt {
      constructor() {
        super(...arguments);
      }

      get isTechnical() {
        const client = this.env.pos.get('client') || this.env.pos.get_client();
        return client?.classification_id[1] === 'TECNICO';
      }

      get hasCoupons() {
        const order = this.env.pos.get_order()
        const bookedCoupons = order.bookedCouponCodes;
        return Object.keys(bookedCoupons).length > 0;
      }

    }

  Registries.Component.extend(OrderReceipt, CustomOrderReceipt);

  return CustomOrderReceipt;

})