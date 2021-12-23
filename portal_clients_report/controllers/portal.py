# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.http import request
from werkzeug.exceptions import Forbidden, NotFound
from odoo.addons.payment.controllers.portal import PaymentPortal
from odoo.exceptions import AccessError, MissingError


class PortalPayment(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(PortalPayment, self)._prepare_portal_layout_values()
        payment_count = request.env['account.payment'].search_count([])
        values['payment_count'] = payment_count
        return values

    @http.route([
        '/my/invoice/paymentss',
        '/my/invoice/paymentss/<model("account.move"):invoice>'
    ], type='http', auth="user", website=True)
    def portal_my_invoice_payments(self, invoice=None, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        AccountInvoice = request.env['account.move'].sudo()
        AccountPayment = request.env['account.payment'].sudo()

        if invoice:
            invoice = AccountInvoice.search([('id', '=', int(invoice))], limit=1)
            if not invoice:
                raise NotFound()
        else:
            invoice = AccountInvoice

        domain = []

        searchbar_sortings = {
            'date': {'label': _('Invoice Date'), 'order': 'create_date desc'},
            'name': {'label': _('Reference'), 'order': 'name desc'},
            'state': {'label': _('Status'), 'order': 'state'},
        }
        # default sort by order
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # count for pager
        payment_count = len(invoice.payment_ids.ids)

        pager = portal_pager(
            url="/my/invoice/payment",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=payment_count,
            step=self._items_per_page
        )

        # payments = AccountPayment.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        payments = invoice.payment_ids
        request.session['my_invoices_history'] = payments.ids[:100]
        attachment_ids = payments.mapped('xml_attach_id').ids or []

        values.update({
            'date': date_begin,
            'payments': payments,
            'attachment_ids': attachment_ids,
            'page_name': 'invoice',
            'pager': pager,
            'default_url': '/my/invoice/payments',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return request.render("portal_clients_report.portal_my_payments", values)

    @http.route(['/my/invoice/payments/<int:payment_id>'], type='http', auth="public", website=True)
    def portal_my_invoice_payment_detail(self, payment_id, access_token=None, report_type=None, download=False, **kw):
        try:
            invoice_sudo = self._document_check_access('account.payment', payment_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=invoice_sudo, report_type=report_type,
                                     report_ref='account.action_report_payment_receipt', download=download)

        # values = self._invoice_get_page_view_values(invoice_sudo, access_token, **kw)
        PaymentPortal.remove_payment_transaction(invoice_sudo.transaction_ids)
        return request.render("portal_clients_report.portal_my_payments", {})
