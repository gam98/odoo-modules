from odoo import http
from odoo.http import request
import base64

class QuoteController(http.Controller):

    @http.route('/quote/download_pdf', type='http', auth="user", methods=['POST'], website=True, csrf=True)
    def download_quote_pdf(self, **kwargs):
        # Recoger los datos enviados desde el modal
        retail_price = kwargs.get('retail_price')
        differentiated_price_for_being_technician = kwargs.get('differentiated_price_for_being_technician')
        price_for_referred_customer = kwargs.get('price_for_referred_customer')

        # Obtener la cotización actual (puedes modificar cómo obtener el pedido según tus necesidades)
        sale_order = request.env['sale.order'].sudo().search([('id', '=', request.session.get('sale_order_id'))], limit=1)

        if sale_order:
            pdf_content = None
            pdf_name = None

            # Generar diferentes PDFs según la opción seleccionada
            if retail_price:
                # Generar PDF para precio de venta al público
                pdf_content, _ = request.env.ref('tkn_technical_quote_generator.action_report_technical_quote_custom').sudo()._render_qweb_pdf([sale_order.id])

                print('odoo----------------------------')
                print(sale_order.read())
                print('odoo----------------------------')
                print(sale_order.order_line.read())
                print('odoo----------------------------')
                # print(sale_order.applied_coupon_ids.read())
                print('odoo----------------------------')
                pdf_name = "Cotización Servicat PVP.pdf"
            elif differentiated_price_for_being_technician:
                # Generar PDF para precio diferenciado por ser técnico
                pdf_content, _ = request.env.ref('tkn_technical_quote_generator.action_report_technical_quote_custom').sudo()._render_qweb_pdf([sale_order.id])
                pdf_name = "Cotización Servicat Técnico.pdf"
            elif price_for_referred_customer:
                # Generar PDF para precio para cliente referido
                pdf_content, _ = request.env.ref('tkn_technical_quote_generator.action_report_technical_quote_custom').sudo()._render_qweb_pdf([sale_order.id])
                pdf_name = "Cotización Servicat Referido.pdf"
            
            # Si se generó contenido PDF, devolverlo como archivo descargable
            if pdf_content and pdf_name:
                pdf_headers = [
                    ('Content-Type', 'application/pdf'),
                    ('Content-Disposition', f'attachment; filename={pdf_name};')
                ]
                return request.make_response(pdf_content, headers=pdf_headers)
        
        # Redireccionar si no hay cotización disponible o no se seleccionó ninguna opción
        return request.redirect('/shop')
