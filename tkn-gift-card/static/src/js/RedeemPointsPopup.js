odoo.define('tkn_gift_card.redeemPointsPopup', function (require) {
  'use strict';

  const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
  const { Gui } = require('point_of_sale.Gui');
  const Registries = require('point_of_sale.Registries');

  class RedeemPointsPopup extends AbstractAwaitablePopup {

    constructor() {
      super(...arguments);
      this.state = {
        pointsToRedeem: this.props.points,  // Inicialmente todos los puntos disponibles
        discountValue: this.calculateDiscount(this.props.points)
      };
    }

    calculateDiscount(points) {
      return points / 100;
    }

    onInputChange(event) {
      const pointsToRedeem = parseInt(event.target.value, 10);
      const discountValue = this.calculateDiscount(pointsToRedeem);

      this.state.pointsToRedeem = pointsToRedeem;
      this.state.discountValue = discountValue;
      this.render();
    }
    async confirm() {
      const pointsToRedeem = parseInt(this.el.querySelector('input[name="pointsToRedeem"]').value, 10);

      if (isNaN(pointsToRedeem) || pointsToRedeem <= 0 || pointsToRedeem > this.props.points) {
        Gui.showPopup('ErrorPopup', {
          title: this.env._t('Cantidad inválida'),
          body: this.env._t('Por favor, ingresa una cantidad válida de puntos a canjear.'),
        });
        return;
      }
      this.resolve({ confirmed: true, payload: { pointsToRedeem } });
    }
  }

  RedeemPointsPopup.template = 'RedeemPointsPopup';

  RedeemPointsPopup.defaultProps = {
    confirmText: 'Canjear',
    cancelText: 'Cancelar',
  };

  Registries.Component.add(RedeemPointsPopup);

  return RedeemPointsPopup;
});
