# -*- coding: utf-8 -*-
# Copyright 2020 Ketan Kachhela <l.kachhela28@gmail.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
	'name': "Account Portal",
	'summary': """Account Portal""",
	'description': """Category Mega Menu""",
	'author': "Ketan Kachhela",
	'website': "l.kachhela28@gmail.com",
	'category': 'Website',
    'version': '15.0',
	'depends': [
		'account',
		'portal',
		'account_reports',
	],
	'data': [
		'security/ir.model.access.csv',
		'views/account_invoice_views.xml',
		'views/templates.xml',
		'views/account_portal_templates.xml'
	],
}
