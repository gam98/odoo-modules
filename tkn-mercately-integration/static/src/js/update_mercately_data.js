odoo.define('tkn-mercately-integration', function (require) {
    "use strict";

    var rpc = require('web.rpc');
  
    var models = require('point_of_sale.models');
    var _super_order = models.Order.prototype;
  
    models.Order = models.Order.extend({

    update_mercately_data: function(){
        const client = this.get_client();
        if (!client) {
            console.log("No hay cliente asociado a la orden.");
            return;
        }
        if (client.classification_id[1] != 'TECNICO') {
            console.log("El cliente no es un técnico. Abortando actualización en Mercately");
            return;
        }
        
        const bookedCoupons = this.bookedCouponCodes;
        const couponKey = Object.keys(bookedCoupons)[0];

        if (couponKey) {
            const programId = bookedCoupons[couponKey].program_id;
            if (programId){
                rpc.query({
                    model: 'pos.order',
                    method: 'get_coupons_program_owner',
                    args: [this,programId]
                }).then((partner) => {
                    this.update_mercately_partner_info(partner[0].id)
                })
            }
        } else {
            this.update_mercately_partner_info(client.id)
        }
    }, 
    
    update_mercately_partner_info: function(client_id) {
        rpc.query({
                model: 'mercately', 
                method: 'update_mercately_partner_info',  
                args: [this, client_id], 
            }).then(function (result) {
                if (result.status === 'success') {
                    console.log('Información del partner actualizada correctamente');
                } else {
                    console.error('Error al actualizar la información del partner');
                }
            }).catch(function (error) {
                console.error('Error en la llamada RPC:', error);
            });
    },

    init: function(attributes) {
        this._super(attributes);
        this.updatedData = false;
    },

    export_for_printing: function(){
        var result = _super_order.export_for_printing.apply(this, arguments);
        if (!this.updatedData) {
            this.update_mercately_data();
            this.updatedData = true;
        }
        return result;
    },

    });
});
