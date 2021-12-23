# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AddDate(models.Model):
    _inherit = 'account.payment'

    date_payment = fields.Date('Fecha Banco')