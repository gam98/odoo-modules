odoo.define('tkn-whatsapp-notification', function (require) {
    "use strict";

    var rpc = require('web.rpc');
  
    var models = require('point_of_sale.models');
    var _super_order = models.Order.prototype;
  
    models.Order = models.Order.extend({

    send_whatsapp: function(){
        this.getSystemParameters().then(({ mercatelyApiUrl, mercatelyApiKey }) => {
            const client = this.get_client();
            if (!client) {
                console.log("No hay cliente asociado a la orden.");
                return;
            }

            const client_name = client.name;
            const client_phone = client.mobile || client.phone;

            // Puntos de lealtad ganados y gastados en esta orden
            const points_won = this.get_won_points(); 
            const points_spent = this.get_spent_points(); 
            const order_amount = this.get_total_with_tax(); ;

            const points_before = client.loyalty_points; 
            const points_after = points_before + points_won - points_spent; 

            const messageData = {
                client_name,
                client_phone,
                points_won,
                points_spent,
                order_amount,
                points_before,
                points_after,
            };

            const messages = this.buildMessages(messageData);
            messages.forEach(message => {
                this.callMercatelyAPI(client_phone, message, mercatelyApiUrl, mercatelyApiKey);
            });     
        });
    },

    trimPhoneNumber: function (phone) {
        if (typeof phone === 'string') {
            return phone.replace(/\D/g, ''); 
        }
        return '';
    },

    buildMessages: function(messageData) {
        
        const greeting = `¡Hola ${messageData.client_name}!👋\n\n`;
        const infoMessage = `Ahora, tu saldo total de puntos es de ${messageData.points_after}.\n\nRecuerda que puedes canjear tus puntos en cualquier momento. Para más información sobre cómo redimir tus puntos, por favor visita este enlace: https://www.repuestoslineablanca.com\n\n¡Esperamos verte pronto! Que tengas un gran día.`;

        if (messageData.order_amount <= 0 && messageData.points_spent > 0){
            const return_order_message = `Has realizado una devolución de productos en Servicat, por lo que hemos restado ${messageData.points_spent} puntos de tu saldo. `
            return [greeting + return_order_message + infoMessage]
        }
        if (messageData.points_spent > 0 && messageData.points_won > 0){
            const points_won_message = `Gracias por tu compra de ${messageData.order_amount}. Con esta transacción, has acumulado ${messageData.points_won} puntos. \n\n`
            const points_spent_message = `Gracias por tu compra de ${messageData.order_amount}. Con esta transacción, has redimido ${messageData.points_spent} puntos. \n\n`
            const total_points_after_adding = `Ahora, tu saldo total de puntos es de ${messageData.points_before + messageData.points_won}.\n\nRecuerda que puedes canjear tus puntos en cualquier momento. Para más información sobre cómo redimir tus puntos, por favor visita este enlace: https://www.repuestoslineablanca.com\n\n¡Esperamos verte pronto! Que tengas un gran día.`;
            return [greeting + points_won_message + total_points_after_adding, greeting + points_spent_message + infoMessage]
        }
        if (messageData.points_spent == 0 && messageData.points_won > 0){
            const points_won_message = `Gracias por tu compra de ${messageData.order_amount}. Con esta transacción, has acumulado ${messageData.points_won} puntos. \n\n`
            return [greeting + points_won_message + infoMessage]
        }

        return [greeting]

    },    

    getSystemParameters: function() {
        const promises = [
            rpc.query({
                model: 'ir.config_parameter',
                method: 'get_param',
                args: ['MERCATELY_API_URL'],
            }),
            rpc.query({
                model: 'ir.config_parameter',
                method: 'get_param',
                args: ['MERCATELY_API_KEY'],
            })
        ];

        return Promise.all(promises).then(function (results) {
            return {
                mercatelyApiUrl: results[0], // URL
                mercatelyApiKey: results[1]  // API Key
            };
        }).catch(function (error) {
            console.error('Error al obtener parámetros del sistema:', error);
        });
    },

    callMercatelyAPI: function(number, message, mercatelyApiUrl, mercatelyApiKey) {
    
        const payload = {
            "phone_number": number,
            "message": message
        };
    
        const headers = {
            "Content-Type": "application/json",
            "api-key": mercatelyApiKey,
            "User-Agent": "My User Agent 1.0"
        };

        console.log({
            "payload": payload,
            "mercatelyApiUrl": mercatelyApiUrl,
            "mercatelyApiKey": mercatelyApiKey,
        })
    
        // fetch(mercatelyApiUrl, {
        //     method: "POST",
        //     headers: headers,
        //     body: JSON.stringify(payload)
        // })
        // .then(response => {
        //     if (!response.ok) {
        //         throw new Error(`Error en la llamada a la API: ${response.statusText}`);
        //     }
        //     return response.json();  // Si la respuesta tiene datos JSON
        // })
        // .then(data => {
        //     console.log('Mensaje enviado exitosamente:', data);
        // })
        // .catch(error => {
        //     console.error('Error al llamar al webhook de WhatsApp:', error);
        // });
    },

    init: function(attributes) {
        this._super(attributes);
        this.messageSent = false; // Variable para rastrear si el mensaje ya fue enviado
    },

    export_for_printing: function(){
        var result = _super_order.export_for_printing.apply(this, arguments);
        if (!this.messageSent) {
            this.send_whatsapp();
            this.messageSent = true; // Actualiza el estado a enviado
        }
        return result;
    },
  
  
    });
});
