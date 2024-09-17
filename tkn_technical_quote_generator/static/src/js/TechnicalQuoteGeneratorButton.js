odoo.define('tkn_technical-quote_generator.TechnicalQuoteGeneratorButton', function (require) {
  'use strict';

  const Registries = require('website_sale.Registries');
  const PosComponent = require('website_sale.PosComponent');
  const { useListener } = require('web.custom_hooks');
  const { Gui } = require('website_sale.Gui');

  class TechnicalQuoteGeneratorButton extends PosComponent {
    constructor() {
      super(...arguments);
      useListener('click', this.onClick);
    }

    clickClose () {
      this.trigger('close-popup');
    }

    onClick() {
      Gui.showPopup('ErrorPopup', {
        title: this.env._t('Error'),
        body: this.env._t('No se ha podido generar la cotización. Por favor, contacte con el administrador del sistema.'),
      })
    }
  }

  TechnicalQuoteGeneratorButton.template = 'TechnicalQuoteGeneratorButton';

  Registries.Component.add(TechnicalQuoteGeneratorButton);

  return TechnicalQuoteGeneratorButton;
})