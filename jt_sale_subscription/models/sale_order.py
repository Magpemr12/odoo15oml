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

from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from odoo.tools import format_date

class SaleOrder(models.Model):

    _inherit = 'sale.order'

    student_id = fields.Many2one('res.partner', string="Student")

    def action_invoice_create(self, grouped=False, final=False):
        res = super(SaleOrder, self).action_invoice_create(grouped=grouped, final=final)
        for inv in res:
            invoice = self.env['account.move'].browse(inv)
            if invoice.student_id:
                for inv_line in invoice.invoice_line_ids:
                    if inv_line.product_id and inv_line.product_id.is_iedu:
                        inv_line.l10n_mx_edi_iedu_id = invoice.student_id
        return res

    @api.onchange('partner_id')
    def onchange_partner(self):
        if self.partner_id and len(self.partner_id.child_ids.ids) > 0:
            student_ids = []
            for student in self.partner_id.child_ids:
                if student.st_alumna:
                    student_ids.append(student.id)
            return {
                'domain': {
                    'student_id': [('id', 'in', student_ids)],
                }
            }

class SaleSubscription(models.Model):

    _inherit = "sale.subscription"

    def _prepare_invoice_data(self):
        self.ensure_one()

        if not self.partner_id:
            raise UserError(_("You must first select a Customer for Subscription %s!") % self.name)

        if 'force_company' in self.env.context:
            company = self.env['res.company'].browse(self.env.context['force_company'])
        else:
            company = self.company_id
            self = self.with_context(force_company=company.id, company_id=company.id)

        fpos_id = self.env['account.fiscal.position'].get_fiscal_position(self.partner_id.id)
        journal = self.template_id.journal_id or self.env['account.journal'].search([('type', '=', 'sale'), ('company_id', '=', company.id)], limit=1)
        if not journal:
            raise UserError(_('Please define a sale journal for the company "%s".') % (company.name or '', ))

        next_date = fields.Date.from_string(self.recurring_next_date)
        if not next_date:
            raise UserError(_('Please define Date of Next Invoice of "%s".') % (self.display_name,))
        periods = {'daily': 'days', 'weekly': 'weeks', 'monthly': 'months', 'yearly': 'years'}
        end_date = next_date + relativedelta(**{periods[self.recurring_rule_type]: self.recurring_interval})
        end_date = end_date - relativedelta(days=1)     # remove 1 day as normal people thinks in term of inclusive ranges.
        addr = self.partner_id.address_get(['delivery', 'invoice'])

        sale_order = self.env['sale.order'].search([('order_line.subscription_id', 'in', self.ids)], order="id desc", limit=1)
        return {
            'account_id': self.partner_id.property_account_receivable_id.id,
            'type': 'out_invoice',
            'partner_id': addr['invoice'],
            'partner_shipping_id': addr['delivery'],
            'currency_id': self.pricelist_id.currency_id.id,
            'journal_id': journal.id,
            'origin': self.code,
            'fiscal_position_id': fpos_id,
            'payment_term_id': sale_order.payment_term_id.id if sale_order else self.partner_id.property_payment_term_id.id,
            'company_id': company.id,
            'comment': _("This invoice covers the following period: %s - %s") % (format_date(self.env, next_date), format_date(self.env, end_date)),
            'user_id': self.user_id.id,
            'invoice_date': self.recurring_next_date,   # Se cambio date_invoice
            'student_id': sale_order.student_id.id if sale_order.student_id else False
        }, sale_order

    def _prepare_invoice(self):
        product_obj = self.env['product.product']
        invoice, sale_order = self._prepare_invoice_data()
        invoice['invoice_line_ids'] = self._prepare_invoice_lines(invoice['fiscal_position_id'])
        if sale_order.student_id:
            for inv_line in invoice['invoice_line_ids']:
                if inv_line[2].get('product_id') and product_obj.browse(inv_line[2].get('product_id')).is_iedu:
                    inv_line[2].update({'l10n_mx_edi_iedu_id': sale_order.student_id.id})
        return invoice
           
