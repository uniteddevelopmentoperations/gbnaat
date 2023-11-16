# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    complaint_type = fields.Selection(
        [('hardware', 'Hardware Problem'), ('software', 'Software Problem'),
         ('connection', 'Connection Problem'), ('security', 'Security Problem'),
         ('os', 'Operating System Problem')], string='Complaint Type')

    def send_ticket_mail(self):
        if self.user_id:
            print('user id')
            display_id = self.id
            print('display_id', display_id)
            action_id = self.env.ref('helpdesk.helpdesk_ticket_view_form').id
            print('action_id', action_id)
            base_url = self.env['ir.config_parameter'].sudo().get_param(
                'web.base.url')
            print('base_url', base_url)
            redirect_link = "/web#id=%s&cids=1&menu_id=121&action=%s" \
                            "&model" \
                            "=helpdesk.ticket&view_type=form" % (
                                display_id, action_id)
            print('redirect_url', redirect_link)
            url = base_url + redirect_link
            print('url', url)
        else:
            raise ValidationError(_("Assign the Ticket"))