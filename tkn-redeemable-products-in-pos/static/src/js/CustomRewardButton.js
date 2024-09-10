odoo.define('tkn_redeemable_products_in_pos.CustomRewardButton', function (require) {
  'use strict';

  const RewardButton = require('pos_loyalty.RewardButton');
  const { useListener } = require('web.custom_hooks');
  const Registries = require('point_of_sale.Registries');

  const CustomRewardButton = RewardButton =>
      class extends RewardButton {
          constructor() {
              super(...arguments);
              useListener('click', this.onClick);
          }

          async hasNonRedeemableProducts() {
            const orders = this.env.pos.get_order().get_orderlines();
            
            const hasNonRedeemableProducts = orders.some(order => order.reward_id === undefined);
      
            if (!hasNonRedeemableProducts) {
              await this.showPopup('ErrorPopup', {
                title: this.env._t('Orden requerida para canje'),
                body: this.env._t('Debe tener al menos un producto en la orden para poder canjear puntos. No es posible canjear puntos sin una orden activa que incluya otros productos.'),
              });

              this.trigger('close-popup');  
            }

            return hasNonRedeemableProducts;
          }

          async handleClientSelection() {
            let order = this.env.pos.get_order();
            let client = this.env.pos.get('client') || this.env.pos.get_client();
      
            if (!client) {
              const { confirmed, payload: newClient } = await this.showTempScreen('ClientListScreen', { client });
              if (confirmed) {
                order.set_client(newClient);
                order.updatePricelist(newClient);
              }

              this.trigger('close-popup');

              return;
            }
      
            if (client.loyalty_points <= 0) {
              await this.showPopup('ErrorPopup', {
                title: this.env._t('Puntos insuficientes'),
                body: this.env._t('Este cliente no tiene puntos suficientes para canjear puntos por productos.'),
              });

              this.trigger('close-popup');

              return false;
            }

            return true;
          }

          async onClick() {
              const hasProducts = await this.hasNonRedeemableProducts();
              
              if (!hasProducts) return;

              const hasClientLoyaltyPoints = await this.handleClientSelection();

              if (!hasClientLoyaltyPoints) return;

              const { confirmed, payload } = await this.showPopup('CustomRewardButtonPopup', {
                  title: this.env._t('Seleccione una opción')
              });

              if (confirmed) {
                  if (payload === 'rewards') {
                      await this.openRewardModal();
                  } else if (payload === 'pvp') {
                      await this.openPVPModal();
                  }
              }

              this.trigger('close-popup');
          }
      }

  Registries.Component.extend(RewardButton, CustomRewardButton);

  return CustomRewardButton;
});
