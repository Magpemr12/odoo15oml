# -*- coding: utf-8 -*-
# Copyright 2020 Ketan Kachhela <l.kachhela28@gmail.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    source_document_rate = fields.Char(string="Source Document Rate", readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['source_document_rate'] = ', s.source_document_rate as source_document_rate'
        groupby += """, s.source_document_rate"""

        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)
