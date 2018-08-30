

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class MrpProduction(models.Model):
    """ Manufacturing Orders """
    _inherit = 'mrp.production'
    
    @api.model
    def create(self, values):
        bom_id = values.get('bom_id')
        bom = self.env['mrp.bom'].browse(bom_id)
        min_qty = bom.product_min_qty
        max_qty = bom.product_max_qty
        
        if values.get('product_qty') < min_qty or values.get('product_qty') > max_qty:
            raise UserError(_('Production quantity should be as per BOM min and max quanities.'))
            
        production = super(MrpProduction, self).create(values)
        return production
    
    @api.onchange('product_id', 'picking_type_id', 'company_id')
    def onchange_product_id(self):
        """ Finds UoM of changed product. """
        res = super(MrpProduction, self).onchange_product_id()
        
        if self.product_id:
            
            bom = self.env['mrp.bom']._bom_find(product=self.product_id, picking_type=self.picking_type_id, company_id=self.company_id.id)
            if bom.type == 'normal':
                self.product_qty = bom.product_max_qty if bom.product_min_qty == bom.product_max_qty else bom.product_min_qty

        return res
