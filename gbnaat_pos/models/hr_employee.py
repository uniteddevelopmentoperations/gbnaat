# -*- coding: utf-8 -*-
from odoo import fields, models


class HrEmployee(models.Model):

    _inherit = 'hr.employee'

    enable_detalles = fields.Boolean(string="Cambiar etiqueta Nota de Cliente", help="Cambiar etiqueta nota de cliente a detalles de prenda")
    enable_folio = fields.Boolean(string="Cambiar etiqueta Nota Interna", help="Cambiar etiqueta nota interna a folio de pedido")
    enable_preimpresion = fields.Boolean(string="Cambiar etiqueta Cuenta", help="Cambiar etiqueta Cuenta a Preimpresión de Recibo")
    disable_comensales = fields.Boolean(string="Deshabilitar botón comensales")
    disable_info = fields.Boolean(string="Deshabilitar botón Información")

