odoo.define('tkn_technical-quote_generator.TechnicalQuoteGeneratorPopup', function (require) {
  'use strict';

  const AbstractAwaitablePopup = require('website_sale.AbstractAwaitablePopup');
  const Registries = require('website_sale.Registries');

  class TechnicalQuoteGeneratorPopup extends AbstractAwaitablePopup {
    constructor() {
      super(...arguments);
    }

    clickClose () {
      this.trigger('close-popup');
    }

    clickOpenPopup() {
      this.trigger('close-popup', { confirmed: true, payload: 'popup' });
    }
  }

  TechnicalQuoteGeneratorPopup.template = 'TechnicalQuoteGeneratorPopup';

  Registries.Component.add(TechnicalQuoteGeneratorPopup);

  return TechnicalQuoteGeneratorPopup;
})