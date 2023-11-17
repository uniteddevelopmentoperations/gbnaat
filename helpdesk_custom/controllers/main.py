# -*- coding: utf-8 -*-
from werkzeug.exceptions import NotFound
from werkzeug.utils import redirect

from odoo.addons.website_helpdesk.controllers.main import WebsiteHelpdesk
from odoo.osv import expression
from odoo.addons.website.controllers.form import WebsiteForm
import base64
from odoo import http, SUPERUSER_ID, _
from odoo.http import request
from odoo.exceptions import ValidationError


class ContactController(WebsiteForm):
    def extract_data(self, model, values):
        dest_model = request.env[model.sudo().model]
        print("Extractinggggggggggggggggggggggggggggggggggggggggggggg",
              dest_model)
        data = {
            'record': {},  # Values to create record
            'attachments': [],  # Attached files
            'custom': '',  # Custom fields values
            'meta': '',  # Add metadata if enabled
        }

        authorized_fields = model.with_user(
            SUPERUSER_ID)._get_form_writable_fields()
        error_fields = []
        custom_fields = []

        for field_name, field_value in values.items():
            print(field_value)
            print(field_name)
            if field_name in ['company_select', 'complaint_type']:
                data['record'][field_name] = field_value
            # If the value of the field if a file
            if hasattr(field_value, 'filename'):
                # Undo file upload field name indexing
                field_name = field_name.split('[', 1)[0]

                # If it's an actual binary field, convert the input file
                # If it's not, we'll use attachments instead
                if field_name in authorized_fields and \
                        authorized_fields[field_name]['type'] == 'binary':
                    data['record'][field_name] = base64.b64encode(
                        field_value.read())
                    field_value.stream.seek(0)  # do not consume value forever
                    if authorized_fields[field_name][
                        'manual'] and field_name + "_filename" in dest_model:
                        data['record'][
                            field_name + "_filename"] = field_value.filename
                else:
                    field_value.field_name = field_name
                    data['attachments'].append(field_value)

            # If it's a known field
            elif field_name in authorized_fields:
                try:
                    input_filter = self._input_filters[
                        authorized_fields[field_name]['type']]
                    data['record'][field_name] = input_filter(self, field_name,
                                                              field_value)
                except ValueError:
                    error_fields.append(field_name)

                if dest_model._name == 'mail.mail' and field_name == 'email_from':
                    # As the "email_from" is used to populate the email_from of the
                    # sent mail.mail, it could be filtered out at sending time if no
                    # outgoing mail server "from_filter" match the sender email.
                    # To make sure the email contains that (important) information
                    # we also add it to the "custom message" that will be included
                    # in the body of the email sent.
                    custom_fields.append((_('email'), field_value))

            # If it's a custom field
            elif field_name != 'context':
                custom_fields.append((field_name, field_value))

        data['custom'] = "\n".join([u"%s : %s" % v for v in custom_fields])

        # Add metadata if enabled  # ICP for retrocompatibility
        if request.env['ir.config_parameter'].sudo().get_param(
                'website_form_enable_metadata'):
            environ = request.httprequest.headers.environ
            data['meta'] += "%s : %s\n%s : %s\n%s : %s\n%s : %s\n" % (
                "IP", environ.get("REMOTE_ADDR"),
                "USER_AGENT", environ.get("HTTP_USER_AGENT"),
                "ACCEPT_LANGUAGE", environ.get("HTTP_ACCEPT_LANGUAGE"),
                "REFERER", environ.get("HTTP_REFERER")
            )

        # This function can be defined on any model to provide
        # a model-specific filtering of the record values
        # Example:
        # def website_form_input_filter(self, values):
        #     values['name'] = '%s\'s Application' % values['partner_name']
        #     return values
        if hasattr(dest_model, "website_form_input_filter"):
            data['record'] = dest_model.website_form_input_filter(request, data[
                'record'])

        missing_required_fields = [label for label, field in
                                   authorized_fields.items() if
                                   field['required'] and label not in data[
                                       'record']]
        if any(error_fields):
            raise ValidationError(error_fields + missing_required_fields)
        print(data)
        # print(z)
        return data


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

        teams = request.env['helpdesk.team'].sudo().search(teams_domain,
                                                           order="id asc")
        if not teams:
            raise NotFound()

        result = self.get_helpdesk_team_data(team or teams[0], search=search)
        result['multiple_teams'] = len(teams) > 1
        print("1111111111122222222222222222222")
        result['companies'] = request.env['res.company'].sudo().search([])
        print('result:', result)
        return request.render("website_helpdesk.team", result)
