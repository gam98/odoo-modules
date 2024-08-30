odoo.define('point_of_sale.ProductScreenExtended', function(require) {
  'use strict';

  const ProductScreen = require('point_of_sale.ProductScreen');
  const Registries = require('point_of_sale.Registries');

  const ProductScreenExtended = ProductScreen => class extends ProductScreen {
      async _onClickPay() {
        var order = this.env.pos.get_order();
          // Calcula los nuevos puntos
        var new_total_points = order.get_new_total_points();

        // Si los puntos son negativos, muestra el popup y no permite continuar
        if (new_total_points < 0) {
            await this.showPopup('ErrorPopup', {
                title: this.env._t('Advertencia'),
                body: this.env._t('No está permitido acumular puntos negativos.'),
            });
            return; // No continuar con la validación
        }

          // Llamar a la implementación original si los puntos no son negativos
          super._onClickPay();
      }
  };

  Registries.Component.extend(ProductScreen, ProductScreenExtended);

  return ProductScreen;
});
