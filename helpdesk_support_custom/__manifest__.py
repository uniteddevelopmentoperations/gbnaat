# -*- coding: utf-8 -*-
{
    'name': "Helpdesk Complaint Register",
    'version': '16.0.1.0.0',
    'summary': """Helpdesk Complaint""",
    'category': 'Inventory/Inventory',
    'depends': ['website_helpdesk'],
    'data': [
        'data/website_menu.xml',
        # 'views/helpdesk_views.xml',
        'views/helpdesk_templates.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
