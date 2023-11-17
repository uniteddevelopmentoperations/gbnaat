# -*- coding: utf-8 -*-
from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request


class WebsiteForm(http.Controller):

    @http.route(['/supportticket'], type='http', auth="user", website=True)
    def support_ticket_page(self):
        companies = request.env['res.company'].sudo().search([])
        helpdesk_team = request.env['helpdesk.team'].sudo().search([])
        print('teams:', helpdesk_team)
        values = {}
        values.update({'companies': companies, 'teams': helpdesk_team})
        return request.render(
            "helpdesk_support_custom.ticket_submit_form_custom", values)

    @http.route(['/supportticket/submit/'], type='http', auth="user",website=True)
    def submit_ticket_form(self, **post):
        print('submit_ticket_form', post)
        partner_name = post.get('partner_name')
        partner_email = post.get('partner_email')
        subject = post.get('name')
        complaint_type = post.get('complaint_type')
        company_select = post.get('company_select')
        teams = post.get('teams')
        if post:
            if company_select == 'gbnaat' or company_select == 'concesionaria' or company_select == 'sistemas' or company_select == 'promotora' or company_select == 'dust' or company_select == 'promociones':
                print('submit_ticket_form')
                request.env['helpdesk.ticket'].sudo().create({
                    # 'partner_id': partner_name.id,
                    'name': subject,
                    'partner_email': partner_email,
                    'complaint_type': complaint_type,
                    'company_select': company_select,
                    'team_id': 21,
                })
            elif company_select == 'rm' or company_select == 'rexmed' or company_select == 'medicar':
                print('submit_ticket_form')
                request.env['helpdesk.ticket'].sudo().create({
                    # 'partner_id': partner_name.id,
                    'name': subject,
                    'partner_email': partner_email,
                    'complaint_type': complaint_type,
                    'company_select': company_select,
                    'team_id': 22,
                })
            else:
                print('submit_ticket_form')
                request.env['helpdesk.ticket'].sudo().create({
                    # 'partner_id': partner_name.id,
                    'name': subject,
                    'partner_email': partner_email,
                    'complaint_type': complaint_type,
                    'company_select': company_select,
                    'team_id': 23,
                })
        return request.render("helpdesk_support_custom.ticket_submited_custom")
