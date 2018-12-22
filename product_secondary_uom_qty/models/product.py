# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today  Technaureus Info Solutions(<http://www.technaureus.com/>).

from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    def _default_sec_uom_id(self, *args):
        return self.env["uom.uom"].search([], limit=1, order='id')[0]
    
    @api.multi
    def convert_to_secondary_uom(self, product, qty):
        #converting to reference uom
        ref_qty = 0
        result = 0
        if product.uom_id.uom_type == 'reference':
            ref_qty = qty
        elif product.uom_id.uom_type == 'bigger':
            ref_qty = qty * product.uom_id.factor_inv
        elif product.uom_id.uom_type == 'smaller':
            ref_qty = qty / product.uom_id.factor
        
        #converting to secondary uom
        if product.sec_uom_id.uom_type == 'reference':
            result = 1 * ref_qty
        elif product.sec_uom_id.uom_type == 'bigger':
            result = ref_qty / product.sec_uom_id.factor_inv
        elif product.sec_uom_id.uom_type == 'smaller':
            result = ref_qty * product.sec_uom_id.factor
        return result
    
    @api.one
    @api.depends('uom_id','sec_uom_id','product_variant_ids','qty_available')
    def _get_secondary_qty_available(self):
        var_ids = []
        for product in self:
            var_ids += [p.id for p in product.product_variant_ids]
        variant_available= self.env['product.product'].browse(var_ids)._product_available()
        for product in self:
            sec_qty_available = 0
            sec_qty_forecast = 0
            for p in product.product_variant_ids:
                sec_qty_available += variant_available[p.id]["qty_available"]
                sec_qty_forecast += variant_available[p.id]["virtual_available"]
                
            if sec_qty_available:
                if product.uom_id == product.sec_uom_id:
                    product.sec_qty_available = sec_qty_available
                else:
                    self.sec_qty_available = round(self.convert_to_secondary_uom(product, sec_qty_available),2)
            else:
                product.sec_qty_available = sec_qty_available
                    
            if sec_qty_forecast:
                if product.uom_id == product.sec_uom_id:
                    product.sec_qty_forecast = sec_qty_forecast
                else:
                    self.sec_qty_forecast = round(self.convert_to_secondary_uom(product, sec_qty_forecast),2)
            else:
                product.sec_qty_forecast = sec_qty_forecast
                
    
    uom_categ_id = fields.Many2one('uom.category', string='UOM Category', 
                                   related='uom_id.category_id')
    sec_uom_id = fields.Many2one('uom.uom', required=True, 
                                 default=_default_sec_uom_id,
                                 string='Secondary Unit of Measure', 
                                 help="Secondary unit of measure used to show \
                                 the qty in this uom.")
    sec_qty_available = fields.Float(compute='_get_secondary_qty_available', 
                                     string='Qty on hand in Secondary UOM')
    sec_qty_forecast = fields.Float(compute='_get_secondary_qty_available', 
                                     string='Forecasted Qty in Secondary UOM')
