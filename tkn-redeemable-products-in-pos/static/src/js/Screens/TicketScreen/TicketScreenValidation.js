odoo.define('tkn_redeemable_products_in_pos.Screens.TicketScreenValidation', function(require) {
  'use strict';

  const TicketScreen = require('point_of_sale.TicketScreen');
  const Registries = require('point_of_sale.Registries');

  const TicketScreenValidation = TicketScreen => class extends TicketScreen {
    async _onDoRefund() {
      const order = this.getSelectedSyncedOrder();

      const customer = order.get_client();

      const allToRefundDetails = this._getRefundableDetails(customer)

      const areProductsRedeemed = allToRefundDetails.some(line => line.orderline.price <= 0);

      if (areProductsRedeemed) {
        await this.showPopup('ErrorPopup', {
          title: this.env._t('Reembolso no permitido'),
          body: this.env._t('No es posible reembolsar productos que ya han sido canjeados. Por favor, revise los productos seleccionados e intente nuevamente.'),
        });
        return;
      }

      super._onDoRefund();
    }
  }

  Registries.Component.extend(TicketScreen, TicketScreenValidation);

  return TicketScreenValidation;
})