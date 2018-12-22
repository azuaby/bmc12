# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

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

    # @api.depends('product_qty', 'price_unit', 'taxes_id', 'volume')
    # def _compute_amount(self):
    #     for line in self:
    #         taxes = line.taxes_id.compute_all(line.price_unit, line.order_id.currency_id, line.product_qty, product=line.product_id, partner=line.order_id.partner_id)
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
    # length = fields.Float(string='Length', digits=dp.get_precision('Length'), default=0.0, compute="_compute_length")
    width = fields.Float(string='Width', digits=dp.get_precision('Width'), default=0.0)
    height = fields.Float(string='Height', digits=dp.get_precision('Height'), default=0.0)
    volume = fields.Float(string='Volume', track_visibility='always', compute="_compute_volume")
    uom_length = fields.Boolean(related='product_uom.length', store=True)
    uom_width = fields.Boolean(related='product_uom.width', store=True)
    uom_height = fields.Boolean(related='product_uom.height', store=True)

    product_template = fields.Many2one(comodel_name='product.template', string="Product Template", required=True)

    @api.onchange('product_template')
    def onchange_product_template(self):
        if self.product_template:
            self.product_id = self.product_template.product_variant_id
            self.length = self.product_template.length

    @api.depends('length', 'width', 'height')
    def _compute_length(self):
        for line in self:
            line.length = line.product_template.length


class Purchase(models.Model):
    _inherit = 'purchase.order'

    @api.multi
    def button_confirm(self):
        order_lines = self.order_line
        # if self.volume > 0.0:
        for order_line in order_lines:
            if order_line.width > 0.0 and order_line.height > 0.0 and order_line.length > 0.0:
                dimension = self.env.ref('product_dimensions.product_attribute_dimensions')
                attribute_values = self.env['product.attribute.value']
                val_name = "{} x {}".format(order_line.width, order_line.height)
                found_attr = attribute_values.search([
                    ('attribute_id', '=', dimension.id),
                    ('name', '=', val_name),
                ])
                if len(found_attr) == 0:
                    vals = {
                        'attribute_id': dimension.id,
                        'name': val_name,
                    }
                    new_values = attribute_values.create(vals)
                    found_attr = new_values

                product_attribute = order_line.product_template.attribute_line_ids

                found = False
                for attr_line in product_attribute:
                    if found_attr.attribute_id == attr_line.attribute_id:
                        found = attr_line.id
                        break
                if found:
                    product_attribute.browse(found).write({
                        'value_ids': [(4, found_attr.ids)],
                    })
                else:
                    product_attribute.create({
                        'attribute_id': dimension.id,
                        'product_tmpl_id': order_line.product_template.id,
                        'value_ids': [(4, found_attr.ids)],
                    })
                order_line.product_template.create_variant_ids()
        return super(Purchase, self).button_confirm()
