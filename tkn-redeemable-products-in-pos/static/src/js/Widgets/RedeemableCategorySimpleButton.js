odoo.define('tkn_redeemable_products_in_pos.RedeemableCategorySimpleButton', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');

    class RedeemableCategorySimpleButton extends PosComponent {}
    RedeemableCategorySimpleButton.template = 'RedeemableCategorySimpleButton';

    Registries.Component.add(RedeemableCategorySimpleButton);

    return RedeemableCategorySimpleButton;
});
