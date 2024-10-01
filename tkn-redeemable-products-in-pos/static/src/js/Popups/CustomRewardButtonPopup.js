odoo.define('tkn_redeemable_products_in_pos.CustomRewardButtonPopup', function (require) {
  'use strict';

  const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
  const Registries = require('point_of_sale.Registries');

  class CustomRewardButtonPopup extends AbstractAwaitablePopup {
    constructor() {
      super(...arguments);
      this.state = {
        points: 0,
      };
      this.env.pos.on('change:clientLoyaltyPoints', this.updatePoints, this);
    }

    clickClose () {
      this.trigger('close-popup');
    }

    willUnmount() {
      this.env.pos.off('change:clientLoyaltyPoints', this.updatePoints, this);
      this.env.pos.set('clientLoyaltyPoints', 0);
    }

    updatePoints() {
      const currentLoyaltyPoints = this.env.pos.get('clientLoyaltyPoints');

      if (!currentLoyaltyPoints) {
        const client = this.env.pos.get_client();
        this.state.points = client.loyalty_points;
        this.env.pos.set('clientLoyaltyPoints', client.loyalty_points);
      } else {
        this.state.points = currentLoyaltyPoints;
      }
    }

    clickReward() {
      this.trigger('close-popup', { confirmed: true, payload: 'rewards' });
      this.openRewardModal();
    }

    clickPVP() {
      this.trigger('close-popup', { confirmed: true, payload: 'pvp' });
      this.openPVPModal();
    }

    async openRewardModal() {

      let order = this.env.pos.get_order();

      const rewards = order.get_available_rewards();
      if (rewards.length === 0) {
        await this.showPopup('ErrorPopup', {
          title: this.env._t('No existen recompensas disponibles'),
          body: this.env._t('No hay recompensas disponibles para este cliente como parte del programa de fidelidad.'),
        });
        return;
      }

      const rewardsList = rewards.map(reward => ({
        id: reward.id,
        label: reward.name,
        item: reward,
      }));

      const { confirmed, payload: selectedReward } = await this.showPopup('SelectionPopup', {
        title: this.env._t('Por favor, seleccione una recompensa'),
        list: rewardsList,
      });
      console.log('********* CustomRewardButtonPopup *********')
      console.log('selectedReward ->', selectedReward);
      console.log('********* CustomRewardButtonPopup *********')

      if (confirmed) {
        order.apply_reward(selectedReward);
      }
    }

    async openPVPModal() {
      const client = this.env.pos.get_client();

      this.updatePoints();

      const points = this.state.points;

      await this.showPopup('RedeemableProductsPopup', {
        title: this.env._t('Canjear productos por puntos'),
        client,
        points,
      });

    }
  }

  CustomRewardButtonPopup.template = 'CustomRewardButtonPopup';

  Registries.Component.add(CustomRewardButtonPopup);

  return CustomRewardButtonPopup;
});
