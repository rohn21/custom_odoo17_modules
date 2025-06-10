# -*- coding: utf-8 -*-
{
    'name': "custom_purchase",

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
    'depends': ['purchase', 'stock', 'account', 'web'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_order_views.xml',   
        'views/report_purchase_quotation_templates.xml',
        'views/report_purchaseorder_document_inherit.xml',
        # 'views/external_layout_templates.xml',
        # 'views/custom_purchase_order_templates.xml',
        # 'report/custom_purchase_report.xml',
        # 'report/custom_purchase_report_layout.xml',
        # 'report/custom_purchase_report_template_inherit.xml',
        'report/purchase_reports.xml',
    ],
    'controllers': [
        'controllers/purchase_controller.py'
    ],
    'installable': True,
    'application': False,
}
