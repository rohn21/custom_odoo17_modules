# -*- coding: utf-8 -*-
{
    'name': "custom_mrp",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    # 'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mrp'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/custom_production_view.xml',
        'views/custom_workorder.xml',
        'reports/custom_ProductionOrder_template_inherit.xml',
        'reports/action_custom_production_order_report.xml',
    ],

    'installable': True,
    'application': False
}

