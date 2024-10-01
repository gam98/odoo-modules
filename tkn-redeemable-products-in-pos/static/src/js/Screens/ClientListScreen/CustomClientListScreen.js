odoo.define('tkn_redeemable_products_in_pos.CustomClientListScreen', function (require) {
  'use strict';

  const ClientListScreen = require('point_of_sale.ClientListScreen');
  const Registries = require('point_of_sale.Registries');

  const CustomClientListScreen = ClientListScreen => class extends ClientListScreen {
    get nextButton() {
      const order = this.env.pos.get_order();
      const hasRewards = order.orderlines.models.some(line => line.hasOwnProperty('reward_id') && line.reward_id !== undefined);

      if (!this.props.client) {

        if (this.state.selectedClient?.classification_id[1] !== 'TECNICO' && hasRewards) {

          this.state.selectedClient = null;

          this.showPopup('ErrorPopup', {
            title: this.env._t('Recompensas No Permitidas'),
            body: this.env._t('Solo los clientes con la clasificación "TECNICO" pueden redimir recompensas. Por favor, seleccione un cliente técnico o elimine las recompensas del pedido.'),
          });

          return { command: 'set', text: this.env._t('Set Custom Client') };
        }

        return { command: 'set', text: this.env._t('Set Custom Client') };

      } else if (this.props.client && this.props.client === this.state.selectedClient) {

        return { command: 'deselect', text: this.env._t('Deselect Custom Client') };

      } else {

        if (this.state.selectedClient.classification_id[1] !== 'TECNICO' && hasRewards) {

          this.showPopup('ErrorPopup', {
            title: this.env._t('Recompensas No Permitidas'),
            body: this.env._t('Solo los clientes con la clasificación "TECNICO" pueden redimir recompensas. Por favor, seleccione un cliente técnico o elimine las recompensas del pedido.'),
          });

          this.state.selectedClient = this.props.client;

          return { command: 'set', text: this.env._t('Change Custom Client') };
        }

        return { command: 'set', text: this.env._t('Change Custom Client') };
      }
    }
  };

  Registries.Component.extend(ClientListScreen, CustomClientListScreen);

  return CustomClientListScreen;
});
