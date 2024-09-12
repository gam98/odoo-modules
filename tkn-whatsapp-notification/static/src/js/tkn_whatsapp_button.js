odoo.define('custom_module.PosOrderCustomButton', function (require) {
    'use strict';

    const PosOrder = require('point_of_sale.ReceiptScreen');
    const rpc = require('web.rpc');
    const Registries = require('point_of_sale.Registries');

    const CustomReceiptScreen = (PosOrder) => class extends PosOrder {
        mounted() {
            super.mounted();
            const buttonsContainer = this.el.querySelector('.actions .buttons');
            if (buttonsContainer) {
                const newButton = document.createElement('div');
                newButton.className = 'button custom-button';
                newButton.innerHTML = '<i class="fa fa-envelope"></i> Send WhatsApp';
                newButton.addEventListener('click', this.sendOrderInfoToWhatsApp.bind(this));
                buttonsContainer.appendChild(newButton);
            }
        }

        sendOrderInfoToWhatsApp() {
            const orderData = {
                partnerId: this.env.pos.attributes.selectedClient.id,
                orderId: this.env.pos.attributes.selectedOrder.uid,
            };

            rpc.query({
                model: 'pos.order',  
                method: 'process_order_and_send_messages',  
                args: [orderData],  
            }).then(function (result) {
                this.showPopup('ConfirmPopup', {
                    title: 'WhatsApp',
                    body: 'Order information sent to WhatsApp!',
                });
            }.bind(this)).catch(function (error) {
                console.error('Error sending WhatsApp message:', error);
            });
        }
    };

    Registries.Component.extend(PosOrder, CustomReceiptScreen);

    return CustomReceiptScreen;
});
