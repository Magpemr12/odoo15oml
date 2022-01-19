
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    generic_customer = fields.Boolean("Generic Customer")
