odoo.define('tkn_redeemable_products_in_pos.RedeemableCategoryBreadcrumb', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');

    class RedeemableCategoryBreadcrumb extends PosComponent {}
    RedeemableCategoryBreadcrumb.template = 'RedeemableCategoryBreadcrumb';

    Registries.Component.add(RedeemableCategoryBreadcrumb);

    return RedeemableCategoryBreadcrumb;
});
