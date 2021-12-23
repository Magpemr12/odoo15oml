# -*- coding: utf-8 -*-
# Copyright 2020 Ketan Kachhela <l.kachhela28@gmail.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import models, fields, api
from odoo.tools.misc import formatLang, format_date
from odoo.tools.translate import _


class AccountFollowupReport(models.AbstractModel):
    _inherit = "account.followup.report"

    def _get_columns_name(self, options):
        """
        Override
        Return the name of the columns of the follow-ups report
        """
        headers = [{},
                   {'name': _('Date'), 'class': 'date', 'style': 'text-align:center; white-space:nowrap;'},
                   {'name': _('Due Date'), 'class': 'date', 'style': 'text-align:center; white-space:nowrap;'},
                   {'name': _('Invoices of the Months of:'), 'class': 'date', 'style': 'text-align:center; white-space:nowrap;'},
                   {'name': _('Concept'), 'class': 'date', 'style': 'text-align:center; white-space:nowrap;'},
                   {'name': _('Source Document'), 'style': 'text-align:center; white-space:nowrap;'},
                   {'name': _('Communication'), 'style': 'text-align:right; white-space:nowrap;'},
                   {'name': _('Expected Date'), 'class': 'date', 'style': 'white-space:nowrap;'},
                   {'name': _('Excluded'), 'class': 'date', 'style': 'white-space:nowrap;'},
                   {'name': _('Total Due'), 'class': 'number o_price_total', 'style': 'text-align:right; white-space:nowrap;'}
                  ]
        if self.env.context.get('print_mode'):
            headers = headers[:5] + headers[7:]  # Remove the 'Expected Date' and 'Excluded' columns
        return headers

    def _get_lines(self, options, line_id=None):
        """
        Override
        Compute and return the lines of the columns of the follow-ups report.
        """
        # Get date format for the lang
        partner = options.get('partner_id') and self.env['res.partner'].browse(options['partner_id']) or False
        if not partner:
            return []
        lang_code = partner.lang or self.env.user.lang or 'en_US'

        lines = []
        res = {}
        today = fields.Date.today()
        line_num = 0
        for l in partner.unreconciled_aml_ids.filtered(lambda l: l.company_id == self.env.user.company_id):
            if l.company_id == self.env.user.company_id:
                if self.env.context.get('print_mode') and l.blocked:
                    continue
                currency = l.currency_id or l.company_id.currency_id
                if currency not in res:
                    res[currency] = []
                res[currency].append(l)
        for currency, aml_recs in res.items():
            total = 0
            total_issued = 0
            for aml in aml_recs:
                amount = aml.amount_residual_currency if aml.currency_id else aml.amount_residual
                invoice_date_due = format_date(self.env, aml.date_maturity or aml.date, lang_code=lang_code)    #Se cambio date_due por invoice_date_due
                total += not aml.blocked and amount or 0
                is_overdue = today > aml.date_maturity if aml.date_maturity else today > aml.date
                is_payment = aml.payment_id
                if is_overdue or is_payment:
                    total_issued += not aml.blocked and amount or 0
                if is_overdue:
                    # Se cambio date_due por invoice_date_due
                    invoice_date_due = {'name': invoice_date_due, 'class': 'color-red date', 'style': 'white-space:nowrap;text-align:center;color: red;'}
                if is_payment:
                    invoice_date_due = ''   #Se cambio date_due por invoice_date_due
                move_line_name = aml.invoice_id.name or aml.name
                invoice_month = aml.invoice_id.x_studio_mes_de_la_factura or ''
                concept = aml.invoice_id.x_studio_concepto or ''
                if self.env.context.get('print_mode'):
                    move_line_name = {'name': move_line_name, 'style': 'text-align:right; white-space:normal;'}
                amount = formatLang(self.env, amount, currency_obj=currency)
                line_num += 1
                expected_pay_date = format_date(self.env, aml.expected_pay_date, lang_code=lang_code) if aml.expected_pay_date else ''
                columns = [
                    format_date(self.env, aml.date, lang_code=lang_code),
                    invoice_date_due,   #Se cambio date_due por invoice_date_due
                    invoice_month,
                    concept,
                    aml.invoice_id._origin, #Se cambio origin
                    move_line_name,
                    expected_pay_date + ' ' + (aml.internal_note or ''),
                    {'name': aml.blocked, 'blocked': aml.blocked},
                    amount,
                ]
                if self.env.context.get('print_mode'):
                    columns = columns[:4] + columns[6:]
                lines.append({
                    'id': aml.id,
                    'invoice_id': aml.invoice_id.id,
                    'view_invoice_id': self.env['ir.model.data'].get_object_reference('account', 'invoice_form')[1],
                    'account_move': aml.move_id,
                    'name': aml.move_id.name,
                    'caret_options': 'followup',
                    'move_id': aml.move_id.id,
                    'type': is_payment and 'payment' or 'unreconciled_aml',
                    'unfoldable': False,
                    'has_invoice': bool(aml.invoice_id),
                    'columns': [type(v) == dict and v or {'name': v} for v in columns],
                })
            total_due = formatLang(self.env, total, currency_obj=currency)
            line_num += 1
            lines.append({
                'id': line_num,
                'name': '',
                'class': 'total',
                'unfoldable': False,
                'level': 0,
                'columns': [{'name': v} for v in [''] * (5 if self.env.context.get('print_mode') else 7) + [total >= 0 and _('Total Due') or '', total_due]],
            })
            if total_issued > 0:
                total_issued = formatLang(self.env, total_issued, currency_obj=currency)
                line_num += 1
                lines.append({
                    'id': line_num,
                    'name': '',
                    'class': 'total',
                    'unfoldable': False,
                    'level': 0,
                    'columns': [{'name': v} for v in [''] * (5 if self.env.context.get('print_mode') else 7) + [_('Total Overdue'), total_issued]],
                })
            # Add an empty line after the total to make a space between two currencies
            line_num += 1
            lines.append({
                'id': line_num,
                'name': '',
                'class': '',
                'unfoldable': False,
                'level': 0,
                'columns': [{} for col in columns],
            })
        # Remove the last empty line
        if lines:
            lines.pop()
        return lines
