# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    complaint_type = fields.Selection(
        [('hardware', 'Hardware Problem'), ('software', 'Software Problem'),
         ('connection', 'Connection Problem'), ('security', 'Security Problem'),
         ('os', 'Operating System Problem'),('odoo','Error de Odoo')], string='Complaint Type')
    company_select = fields.Selection([
                    ('gbnaat', 'GB Soluciones Naat, S. de R.L. de C.V'),
                    ('concesionaria', 'Concesionaria El Encierro del Norte, S. de R.L. de C.V'),
                    ('sistemas', 'Sistemas Industrializados en Comedores, S. de R.L. de C.V'),
                    ('promotora', 'Promotora Misiones del Norte, S. de R.L. de C.V'),
                    ('dust', 'Dust Tex de Mexico, SA de CV'),
                    ('promociones', 'Promociones Delta Juarez S.A. de C.V.'),
                    ('rm', 'RM HealthCare Products S.A. de C.V.'),
                    ('rexmed', 'PJ Rex MED LLC.'),
                    ('medicar', 'Medicar Health Inc.'),
                    ('mp','M&P Logictics LLC'),
                    ('promisa', 'PROVEEDORA DE MATERIAL INDUSTRIAL'),
                    ('dmd', 'DMD CUSTOM CRATES & BOXES INC.'),
                    ], string='Compañía Origen')
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



class HelpdeskTeam(models.Model):
    _inherit = "helpdesk.team"

    
    def method_update(self):
        print("Update")
        teams = self.filtered('use_website_helpdesk_form')
        default_form = self.env.ref(
            'helpdesk_custom.ticket_submit_form_custom').sudo().arch
        for team in teams:
            print(team.website_form_view_id.id)
            team.website_form_view_id.unlink()
            xmlid = 'website_helpdesk.team_form_' + str(team.id)
            form_template = self.env['ir.ui.view'].sudo().create({
                'type': 'qweb',
                'arch': default_form,
                'name': xmlid,
                'key': xmlid
            })
            self.env['ir.model.data'].sudo().create({
                'module': 'website_helpdesk',
                'name': xmlid.split('.')[1],
                'model': 'ir.ui.view',
                'res_id': form_template.id,
                'noupdate': True
            })
            team.website_form_view_id = form_template.id
            print('44444444444444444444444')

    def _ensure_submit_form_view(self):

        teams = self.filtered('use_website_helpdesk_form')
        if not teams:
            return

        default_form = self.env.ref(
            'helpdesk_custom.ticket_submit_form_custom').sudo().arch
        for team in teams:
            if not team.website_form_view_id:
                xmlid = 'website_helpdesk.team_form_' + str(team.id)
                form_template = self.env['ir.ui.view'].sudo().create({
                    'type': 'qweb',
                    'arch': default_form,
                    'name': xmlid,
                    'key': xmlid
                })
                self.env['ir.model.data'].sudo().create({
                    'module': 'website_helpdesk',
                    'name': xmlid.split('.')[1],
                    'model': 'ir.ui.view',
                    'res_id': form_template.id,
                    'noupdate': True
                })
                team.website_form_view_id = form_template.id
