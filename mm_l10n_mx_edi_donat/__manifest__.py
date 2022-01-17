# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'EDI Complement for Mexico Donations',
    'version': '15.0.1.0.0',
    "license": "LGPL-3",
    "author": "Vauxoo",
    'category': 'Hidden',
    'summary': 'Mexican Localization for EDI documents',
    'depends': [
        'l10n_mx_edi_extended',
        'l10n_mx_edi_donat',
    ],
    'data': [
        "data/donations.xml",
        "views/res_partner_view.xml",

        "views/product_view.xml",
        "views/invoice_view.xml",
        "views/invoice_report.xml",
        "data/partner.xml"
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
}
