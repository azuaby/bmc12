# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('length', 'width', 'height')
    def _compute_volume(self):
        volume = 0.0
        for line in self:
            if line.length:
                volume = line.length
            if line.height:
                volume = line.height
            if line.width:
                volume = line.width
            if line.length and line.width:
                volume = line.length * line.width
            if line.height and line.width:
                volume = line.height * line.width
            if line.length and line.height:
                volume = line.height * line.length
            if line.length and line.width and line.height:
                volume = line.height * line.length * line.width
            line.volume = volume

    # @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'volume')
    # def _compute_amount(self):
    #     """
    #     Compute the amounts of the SO line.
    #     """
    #     for line in self:
    #         price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
    #         taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty,
    #                                         product=line.product_id, partner=line.order_id.partner_id)
    #         if line.volume:
    #             total_excluded = taxes['total_excluded'] * line.volume
    #             total_included = taxes['total_included'] * line.volume
    #             line.update({
    #                 'price_tax': total_included - total_excluded,
    #                 'price_total': total_included,
    #                 'price_subtotal': total_excluded,
    #             })
    #         else:
    #             line.update({
    #                 'price_tax': taxes['total_included'] - taxes['total_excluded'],
    #                 'price_total': taxes['total_included'],
    #                 'price_subtotal': taxes['total_excluded'],
    #             })

    length = fields.Float(string='Length', digits=dp.get_precision('Length'), default=0.0)
    width = fields.Float(string='Width', digits=dp.get_precision('Width'), default=0.0)
    height = fields.Float(string='Height', digits=dp.get_precision('Height'), default=0.0)
    volume = fields.Float(string='Volume', track_visibility='always', compute="_compute_volume")
    uom_length = fields.Boolean(related='product_uom.length', store=True)
    uom_width = fields.Boolean(related='product_uom.width', store=True)
    uom_height = fields.Boolean(related='product_uom.height', store=True)

    product_template = fields.Many2one(comodel_name='product.template', string="Product Template ID", required=True)
    product_quantity = fields.Float(string='Product Qty', digits=dp.get_precision('Product Unit of Measure'), required=True, default=1.0)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    length = fields.Float(string='Length', digits=dp.get_precision('Length'), default=0.0)


class ProductUOM(models.Model):
    _inherit = "uom.uom"

    is_enable = fields.Boolean(string="Product Dimensions Enable in Order line")
    length = fields.Boolean(string="Length")
    width = fields.Boolean(string="Width")
    height = fields.Boolean(string="Height")

    @api.onchange('is_enable')
    def onchange_is_enable(self):
        for res in self:
            if not res.is_enable:
                res.length = False
                res.width = False
                res.height = False
