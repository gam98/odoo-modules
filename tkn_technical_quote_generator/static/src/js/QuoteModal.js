odoo.define('tkn_technical_quote_generator.QuoteModal', function (require) {
  "use strict";

  const ajax = require('web.ajax');

  $(document).ready(function () {
      $('#quote_form').on('submit', function (e) {
          e.preventDefault();

          // Serializar los valores del formulario
          var formData = $(this).serialize();

          // Enviar datos mediante AJAX
          ajax.post('/quote/download_pdf', formData).then(function (response) {
              if (response.success) {
                  // Redirigir para descargar el PDF
                  window.open(response.download_url, '_blank');
              } else {
                  alert('Error al generar la cotización.');
              }
          });
      });
  });
});
