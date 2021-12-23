# -*- coding: utf-8 -*-
# Copyright 2020 Ketan Kachhela <l.kachhela28@gmail.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import models, fields, api, _


class AccountInvoice(models.Model):
    _inherit = 'account.move'   # Se modifico account.invoice

    discount_amount = fields.Float('Discount Amount', compute='_compute_discount_amount', store=True)

    @api.depends('invoice_line_ids', 'invoice_line_ids.discount')
    def _compute_discount_amount(self):
        for rec in self:
            total = 0.0
            for line in rec.invoice_line_ids:
                total += line.price_subtotal + line.price_unit * ((line.discount or 0.0) / 100.0) * line.quantity
            rec.discount_amount = total - rec.amount_untaxed
