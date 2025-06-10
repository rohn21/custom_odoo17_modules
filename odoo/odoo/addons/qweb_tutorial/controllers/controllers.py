# -*- coding: utf-8 -*-
from odoo import http

class QwebTutorial(http.Controller):
    @http.route('/qweb-tutorial/', auth='public', website=True)
    def index(self, **kw):
        return http.request.render('qweb_tutorial.qweb_html')
        # return "This is the tutorial page using controller"