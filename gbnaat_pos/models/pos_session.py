# -*- coding: utf-8 -*-

from odoo import models


class PosSession(models.Model):

    _inherit = 'pos.session'

    def _loader_params_hr_employee(self):
        result = super()._loader_params_hr_employee()
        result['search_params']['fields'].extend(
            ['enable_detalles', 'enable_folio', 'enable_preimpresion', 'disable_comensales', 'disable_info'])
        return result
