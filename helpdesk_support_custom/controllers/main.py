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
        company_id = post.get('company_id')
        teams = post.get('teams')
        if post:
            print('submit_ticket_form')
            request.env['helpdesk.ticket'].sudo().create({
                # 'partner_id': partner_name.id,
                'name': subject,
                'partner_email': partner_email,
                'complaint_type': complaint_type,
                'company_id': company_id,
            })
        return request.render("helpdesk_support_custom.ticket_submited_custom")
