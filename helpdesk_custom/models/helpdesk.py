# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    complaint_type = fields.Selection(
        [('hardware', 'Hardware Problem'), ('software', 'Software Problem'),
         ('connection', 'Connection Problem'), ('security', 'Security Problem'),
         ('os', 'Operating System Problem')], string='Complaint Type')


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
