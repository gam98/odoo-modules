from odoo import models, fields, api

class TechnicalQuote(models.Model):
    _name = 'technical.quote.generator'

    def action_report(self):
        print('odoo----------------------------')
        return self.env.ref('tkn_technical_quote_generator.action_report_technical_quote').report_action(self)

    def print_technical_quote_report(self):
        data = {
            'model_id': self.id,
            'to_date': self.to_date,
            'from_date': self.from_date,
            'customer_id': self.customer_id.id,
            'customer_name': self.customer_id.name
        }
        return self.env.ref('module_name.action_report_technical_quote').report_action(self, data=data)

class TechnicalQuoteReport(models.AbstractModel):
    _name = 'report.technical_quote_generator.report_technical_quote'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['technical.quote.generator'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'technical.quote.generator',
            'docs': docs,
            'data': data,
        }