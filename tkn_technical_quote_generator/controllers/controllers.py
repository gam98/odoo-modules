from odoo import http
from odoo.http import request

class QuoteController(http.Controller):

    @http.route('/quote/download_pdf', type='http', auth="user", methods=['POST'], website=True, csrf=True)
    def download_quote_pdf(self, **kwargs):
        quote_type = kwargs.get('quote_type')

        sale_order = request.env['sale.order'].sudo().search([('id', '=', request.session.get('sale_order_id'))], limit=1)

        if sale_order:
            pdf_content = None
            pdf_name = None

            if quote_type == 'retail_price':
       
                pdf_content, _ = request.env.ref('tkn_technical_quote_generator.action_report_retail_price').sudo()._render_qweb_pdf([sale_order.id])
                pdf_name = "Cotización Servicat PVP.pdf"

            elif quote_type == 'differentiated_price_for_being_technician':
                
                pdf_content, _ = request.env.ref('tkn_technical_quote_generator.action_report_differentiated_price_for_being_technician').sudo()._render_qweb_pdf([sale_order.id])
                pdf_name = "Cotización Servicat Técnico.pdf"
                
            elif quote_type == 'price_for_referred_customer':
                
                pdf_content, _ = request.env.ref('tkn_technical_quote_generator.action_report_price_for_referred_customer').sudo()._render_qweb_pdf([sale_order.id])
                pdf_name = "Cotización Servicat Referido.pdf"
            
            if pdf_content and pdf_name:
                pdf_headers = [
                    ('Content-Type', 'application/pdf'),
                    ('Content-Disposition', f'attachment; filename={pdf_name};')
                ]
                return request.make_response(pdf_content, headers=pdf_headers)
        
        return request.redirect('/shop')
