# -*- coding: utf-8 -*-
# Copyright 2020 Ketan Kachhela <l.kachhela28@gmail.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import models, fields, api, _


class AccountInvoice(models.Model):
    _inherit = 'account.move'    #Se cambio 'account.invoice'

    pricelist_id = fields.Many2one('product.pricelist', 'Pricelist', readonly=True)
