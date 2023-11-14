# -*- coding: utf-8 -*-
from werkzeug.exceptions import NotFound
from werkzeug.utils import redirect
from odoo import http
from odoo.http import request
from odoo.addons.website_helpdesk.controllers.main import WebsiteHelpdesk
from odoo.osv import expression


class WebsiteHelpdeskInherit(WebsiteHelpdesk):

    @http.route(['/helpdesk', '/helpdesk/<model("helpdesk.team"):team>'],
                type='http', auth="public", website=True, sitemap=True)
    def website_helpdesk_teams(self, team=None, **kwargs):
        print("111111111111111111111111")
        search = kwargs.get('search')

        teams_domain = [('use_website_helpdesk_form', '=', True)]
        if not request.env.user.has_group('helpdesk.group_helpdesk_manager'):
            if team and not team.is_published:
                raise NotFound()
            teams_domain = expression.AND(
                [teams_domain, [('website_published', '=', True)]])

        if team and team.show_knowledge_base and not kwargs.get('contact_form'):
            return redirect(team.website_url + '/knowledgebase')

        teams = request.env['helpdesk.team'].search(teams_domain,
                                                    order="id asc")
        if not teams:
            raise NotFound()

        result = self.get_helpdesk_team_data(team or teams[0], search=search)
        result['multiple_teams'] = len(teams) > 1
        result['companies'] = request.env['res.company'].search([])
        print('result:', result)
        return request.render("website_helpdesk.team", result)
