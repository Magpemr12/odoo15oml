from odoo import api, fields, models, _

class AccountInvoice(models.Model):

    _inherit = 'account.move'   # Se modifico account.invoice

    surcharge_related_inv = fields.Char("Factura relacionada al recargo")

    def action_general(self):
        for invoice in self:
            if invoice.state == 'open' and not invoice.payment_ids and invoice.type == 'out_invoice' and \
                  not invoice.surcharge_related_inv:
                part = invoice.partner_id
                surcharge_inv = invoice.copy()
                surcharge_inv.invoice_line_ids = [(5, 0)]
                surcharge_inv.surcharge_related_inv = invoice.number
                line_vals = []
                fpos = invoice.fiscal_position_id
                is_invoice_line = False
                for line in invoice.invoice_line_ids:
                    if line.product_id and not line.product_id.is_surcharge and line.product_id.related_product:
                        is_invoice_line = True
                        prod = line.product_id
                        related_prod = prod.related_product
                        # unit_price = line.price_unit
                        surcharge = 0
                        if prod.prcntg_surchg_apply != 0:
                            surcharge = line.price_subtotal * prod.prcntg_surchg_apply
                        accounts = related_prod.product_tmpl_id.get_product_accounts(fpos)
                        account = False
                        if accounts:
                            account = accounts['income']
                        product_name = related_prod.partner_ref
                        if related_prod.description_sale:
                            product_name += '\n' + related_prod.description_sale
                        name = related_prod.name
                        if product_name != None:
                            name = product_name
                        taxes = related_prod.taxes_id.filtered(lambda r: r.company_id == invoice.company_id) or\
                                account.tax_ids or invoice.company_id.account_sale_tax_id
                        line_vals.append({
                            'product_id': related_prod,
                            'price_unit': surcharge,
                            'name': name,
                            'uom_id': related_prod.uom_id if related_prod.uom_id else False,
                            'account_id': account,
                            'invoice_line_tax_ids': invoice.fiscal_position_id.map_tax(taxes, related_prod, part)
                        })
                if not is_invoice_line:
                    surcharge_inv.unlink()
                if is_invoice_line:
                    surcharge_inv.invoice_line_ids = [(0, 0, val) for val in line_vals]
                    surcharge_inv._onchange_invoice_line_ids()
                    surcharge_inv._compute_amount()

