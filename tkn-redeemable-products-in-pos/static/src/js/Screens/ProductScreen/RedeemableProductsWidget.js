odoo.define('tkn_redeemable_products_in_pos.RedeemableProductsWidget', function (require) {
  'use strict';

  const { useState } = owl.hooks;
  const PosComponent = require('point_of_sale.PosComponent');
  const { useListener } = require('web.custom_hooks');
  const Registries = require('point_of_sale.Registries');

  class RedeemableProductsWidget extends PosComponent {

    constructor() {
      super(...arguments);
      useListener('switch-category-id', this._switchCategoryId);
      useListener('update-search', this._updateSearch);
      useListener('try-add-product', this._tryAddProduct);
      useListener('clear-search', this._clearSearch);
      useListener('update-product-list', this._updateProductList);
      this.state = useState({ searchWord: '', selectedCategoryId: this.env.pos.db.root_category_id, });
    }
    willUnmount() {
      this.trigger('toggle-mobile-searchbar', false);
    }
    get selectedCategoryId() {
      return this.state.selectedCategoryId;
    }
    get searchWord() {
      return this.state.searchWord.trim();
    }
    get productsToDisplay() {
      let list = [];
      if (this.searchWord !== '') {
        list = this.env.pos.db.search_product_in_category(
          this.selectedCategoryId,
          this.searchWord
        );
      } else {
        list = this.env.pos.db.get_product_by_category(this.selectedCategoryId);
      }

      console.log('********* RedeemableProductsWidget *********')
      console.log('list ->', list.sort(function (a, b) { return a.display_name.localeCompare(b.display_name) }));
      console.log('********* RedeemableProductsWidget *********')

      return list.sort(function (a, b) { return a.display_name.localeCompare(b.display_name) });
    }
    get subcategories() {
      return this.env.pos.db
        .get_category_childs_ids(this.selectedCategoryId)
        .map(id => this.env.pos.db.get_category_by_id(id));
    }
    get breadcrumbs() {
      if (this.selectedCategoryId === this.env.pos.db.root_category_id) return [];
      return [
        ...this.env.pos.db
          .get_category_ancestors_ids(this.selectedCategoryId)
          .slice(1),
        this.selectedCategoryId,
      ].map(id => this.env.pos.db.get_category_by_id(id));
    }
    get hasNoCategories() {
      return this.env.pos.db.get_category_childs_ids(0).length === 0;
    }
    _switchCategoryId(event) {
      this.state.selectedCategoryId = event.detail; 
    }
    _updateSearch(event) {
      this.state.searchWord = event.detail;
    }
    _tryAddProduct(event) {
      const searchResults = this.productsToDisplay;
      // If the search result contains one item, add the product and clear the search.
      if (searchResults.length === 1) {
        const { searchWordInput } = event.detail;
        this.trigger('click-product', searchResults[0]);
        // the value of the input element is not linked to the searchWord state,
        // so we clear both the state and the element's value.
        searchWordInput.el.value = '';
        this._clearSearch();
      }
    }
    _clearSearch() {
      this.state.searchWord = '';
    }
    _updateProductList(event) {
      this.render();
      this.trigger('switch-category-id', 0);
    }
  }
  RedeemableProductsWidget.template = 'RedeemableProductsWidget';

  Registries.Component.add(RedeemableProductsWidget);

  return RedeemableProductsWidget;
});
