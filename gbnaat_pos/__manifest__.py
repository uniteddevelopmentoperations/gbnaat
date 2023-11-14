# -*- coding: utf-8 -*-
{
    'name': "GBNAAT ERP Instance",
    'author': "Juárez Technology",
    'summary': """
        Módulos de Gbnaat.
    """,
    'website': "http://www.juarez.technology",
    "license": "LGPL-3",
    'category': 'Gbnaat',
    'version': '16.0',
    'depends': ['base', 'hr', 'point_of_sale', 'pos_hr'],
    'data': [
        'views/hr_employee_views.xml',
        ],
    'qweb': [],
    'assets':{
        'point_of_sale.assets': [
            'gbnaat_pos/static/src/xml/*',
            'gbnaat_pos/static/src/js/*',
        ],
    }
    
}
