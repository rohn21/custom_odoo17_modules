# -*- coding: utf-8 -*-
{
    'name': "qweb_tutorial",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'calendar', 'website'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'views/views.xml',
        'views/qweb_template.xml',
        'views/custom_webpage_view.xml',
        # 'views/custom_calendar_view.xml',
        'views/custom_calendar_backend.xml', #with custom_model, view(xml)
        'views/render_calendar.xml',  #with custom_model, view(xml)
        'views/custom_booking_template.xml',
        'data/sample_booking_data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

'controllers': [
        'controllers/controllers.py'
    ],
}

