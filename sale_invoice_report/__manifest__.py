# -*- coding: utf-8 -*-
# Copyright 2020 Ketan Kachhela <l.kachhela28@gmail.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Sale Invoice Report',
    'version': '15.0',
    'summary': """
Add field for rate which passes from SO to Invoice and use in Sale Report
    """,
    'category': 'Sales',
    'depends': [
        'sale',
        'sale_subscription',
        'account',
        'sale_enterprise',
        'jt_sale_subscription'
    ],
    'data': [
        'views/account_invoice_views.xml'
    ],
    'images': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
