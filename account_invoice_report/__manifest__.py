# -*- coding: utf-8 -*-
# Copyright 2020 Ketan Kachhela <l.kachhela28@gmail.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Invoice Report Discount',
    'version': '15.0',
    'summary': """
    """,
    'author': "Ketan Kachhela",
    'website': "<L.KACHHELA28@GMAIL.COM>",
    'category': 'Sales',
    'depends': [
        'sale',
        'sale_subscription',
        'account',
        'sales_team'
    ],
    'data': [
        'report/account_invoice_report_views.xml'
    ],
    'images': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
