# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class account_payment(models.Model):
    _name = "account.payment"
    #_inherit = ['portal.mixin', 'account.payment', 'mail.thread', 'account.abstract.payment']
    _inherit = ['portal.mixin', 'account.payment', 'mail.thread']

    def _compute_access_url(self):
        super(account_payment, self)._compute_access_url()
        for payment in self:
            payment.access_url = '/my/invoice/payments/%s' % (payment.id)

    def _compute_xml_attach_id(self):
        IrAttachment = self.env['ir.attachment']
        for rec in self:
            attch_id = IrAttachment.search([
                ('res_id', '=', rec.id),
                ('res_model', '=', 'account.payment'),
                ('type', '=', 'binary'),
                ('mimetype', 'in', ['application/xml', 'text/plain'])
            ], limit=1)
            rec.xml_attach_id = attch_id if attch_id else False

    def _compute_pdf_attach_id(self):
        IrAttachment = self.env['ir.attachment']
        for rec in self:
            attch_id = IrAttachment.search([
                ('res_id', '=', rec.id),
                ('res_model', '=', 'account.payment'),
                ('type', '=', 'binary'),
                ('mimetype', '=', 'application/pdf')
            ], limit=1)
            rec.xml_attach_id = attch_id if attch_id else False

    xml_attach_id = fields.Many2one('ir.attachment', compute="_compute_xml_attach_id", string="Attachment")
    pdf_attach_id = fields.Many2one('ir.attachment', compute="_compute_xml_attach_id", string="Attachment")
