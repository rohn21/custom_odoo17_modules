# -*- coding: utf-8 -*-
{
    'name': "Custom Sales Extension",

    'summary': "Adds extra fields to Sales Quotation",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale_management', 'sale_stock', 'account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/report_display_barcode.xml',
        'views/report_display_actions.xml',
        'views/report_saleorder_inherit.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],


    'controllers': [
        'controllers/controllers.py'
    ],

    'installable': True,
    'application': True,
}

