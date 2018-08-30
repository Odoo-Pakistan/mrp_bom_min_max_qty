
from odoo import models, api, fields, _
from odoo.addons import decimal_precision as dp

class MrpBom(models.Model):
    """ Defines bills of material for a product or a product template """
    _inherit = 'mrp.bom'
    
    product_min_qty = fields.Float(
        'Minimum Quantity', digits=dp.get_precision('Product Unit of Measure'),
        help="Minimum allowed quanity for production.")
    product_max_qty = fields.Float(
        'Maximum Quantity', digits=dp.get_precision('Product Unit of Measure'),
        help="Maximum allowed quantity for production. Keep Maximum and Minimum quanities same to force fix production quantity.")
    
    _sql_constraints = [
        ('product_min_qty', 'CHECK( product_min_qty > 0 )', 'Minimum Qty must be greater than zero.'),
        ('product_max_qty', 'CHECK( product_max_qty > 0 )', 'Maximum Qty must be greater than zero.'),
    ]