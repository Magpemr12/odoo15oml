from odoo import api, fields, models, _

class Producttemplate(models.Model):

    _inherit = 'product.template'

    is_surcharge = fields.Boolean(string='Es Un recargo')
    related_product = fields.Many2one('product.product', string='Producto Relacionado')
    apply_surcharge = fields.Boolean(string='Aplicar recargo.')
    prcntg_surchg_apply = fields.Float(string='% de Recargo.')