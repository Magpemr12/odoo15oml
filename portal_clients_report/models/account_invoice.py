# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class AccountInvoice(models.Model):
    _inherit = 'account.move'   # Se cambio 'account.invoice'

    #Se cambio date_invoice por invoice_data
    #Se cambio rec por record
    @api.depends('invoice_date')
    def _compute_invoice_month(self):
        for record in self:
            if record.invoice_date:
                record.invoice_month = record.invoice_date.strftime("%B")
            else:
                record.invoice_month = ""

    def _compute_xml_attach_id(self):
        IrAttachment = self.env['ir.attachment']
        for record in self:
            attch_id = IrAttachment.search([
                ('res_id', '=', record.id), #Se cambio rec.ide
                ('res_model', '=', 'account.move'), #Se cambio account.invoice
                ('type', '=', 'binary'),
                ('mimetype', 'in', ['application/xml', 'text/plain'])
            ], limit=1)
            record.xml_attach_id = attch_id if attch_id else False  #Se cambio rec.xml_attach_id

    invoice_month = fields.Char(string="Invoices of the Months of:", compute="_compute_invoice_month")
    concept = fields.Char(string="Concept")
    xml_attach_id = fields.Many2one('ir.attachment', compute="_compute_xml_attach_id", string="Attachment")
