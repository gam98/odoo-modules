odoo.define('tkn_gift_card.GiftCardValueDisplay', function (require) {
  'use strict';

  const PosComponent = require('point_of_sale.PosComponent');
  const { useListener } = require('web.custom_hooks');
  const Registries = require('point_of_sale.Registries');

  class GiftCardValueDisplay extends PosComponent {
    constructor() {
      super(...arguments);
      this.state = {
        giftCardValue: 0,
      };
      this.env.pos.on('change:gift_card_value', this.updateGiftCardValue.bind(this));
      console.log(this.state.giftCardValue);
    }

    updateGiftCardValue(giftCardValue) {
      this.state.giftCardValue = giftCardValue;
      this.render();
    }

    get giftCardValue() {
      return this.state.giftCardValue;
    }
  }

  GiftCardValueDisplay.template = 'GiftCardValueDisplay';

  Registries.Component.add(GiftCardValueDisplay);

  return GiftCardValueDisplay;
});
