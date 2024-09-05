odoo.define('tkn_redeemable_products_in_pos.RedeemableCategoryButton', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');

    class RedeemableCategoryButton extends PosComponent {
        get imageUrl() {
            const category = this.props.category
            return `/web/image?model=pos.category&field=image_128&id=${category.id}&write_date=${category.write_date}&unique=1`;
        }
    }
    RedeemableCategoryButton.template = 'RedeemableCategoryButton';

    Registries.Component.add(RedeemableCategoryButton);

    return RedeemableCategoryButton;
});
