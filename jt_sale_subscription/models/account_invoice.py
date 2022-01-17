# -*- coding: utf-8 -*-
##############################################################################
#
#    Jupical Technologies Pvt. Ltd.
#    Copyright (C) 2018-TODAY Jupical Technologies(<http://www.jupical.com>).
#    Author: Jupical Technologies Pvt. Ltd.(<http://www.jupical.com>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import fields, models, api

class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _create_invoice(self, order, so_line, amount):
        res = super(SaleAdvancePaymentInv, self)._create_invoice(order=order, so_line=so_line, amount=amount)
        if res and res.student_id:
            for inv_line in res.invoice_line_ids:
                if inv_line.product_id and inv_line.product_id.is_iedu:
                    inv_line.l10n_mx_edi_iedu_id = res.student_id.id
        return res
        
class AccountInvoice(models.Model):

    _inherit = 'account.move'   # Se cambio 'account.invoice'

    sale_id = fields.Many2one('sale.order', string="Sale Order ID")
    student_id = fields.Many2one('res.partner', string="Student")
    # origin = fields.Char(string='Source Document',
    #                      help="Reference of the document that produced this invoice.",
    #                      readonly=True, states={'draft': [('readonly', False)]})

    @api.model
    def create(self, vals):
        res = super(AccountInvoice, self).create(vals)
        if res.invoice_origin:  # Se cambio origin
            order = self.env['sale.order'].search([('name', '=', res.invoice_origin)])
            if order:
                res.sale_id = order.id
                res.student_id = order.student_id and order.student_id.id or False
        return res

    @api.onchange('student_id')
    def _onchange_student_id(self):
        if self.student_id:
            for line in self.invoice_line_ids:
                if line.product_id and line.product_id.is_iedu:
                    # Field already added to system from frontend
                    line.l10n_mx_edi_iedu_id = self.student_id.id
