# -*- coding: utf-8 -*-

from odoo import models, fields, api


class GradeComputableMixin(models.AbstractModel):
    _name = 'grade.computable.mixin'
    _description = 'Grade Computable Mixin'
    marks_obtained = fields.Float(string='Marks Obtained', required=True)
    grade = fields.Char(string='Grade', compute='_compute_grade', store=True)

    @api.depends('marks_obtained')
    def _compute_grade(self):
        for record in self:
            marks = record.marks_obtained
            if 90 <= marks <= 100:
                record.grade = 'A+'
            elif 80 <= marks < 90:
                record.grade = 'A'
            elif 70 <= marks < 80:
                record.grade = 'B'
            elif 60 <= marks < 70:
                record.grade = 'C'
            else:
                record.grade = 'D'


class ApprovalMixin(models.AbstractModel):
    _name = 'approval.mixin'
    _description = 'Approval Mixin for student models'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], default='draft', string='Approval Status', tracking=True)

    def action_approve(self):
        self.ensure_one()
        if not self.user_has_groups('custom_school.group_student_approver'):
            raise PermissionError("Only approvers can approve students.")
        self.state = 'approved'

    def action_reject(self):
        self.ensure_one()
        if not self.user_has_groups('custom_school.group_student_approver'):
            raise PermissionError("Only approvers can reject students.")
        self.state = 'rejected'


class ClassAStudent(models.Model):
    _name = 'class_a.student'
    _description = 'Class A Student'
    _inherit = ['grade.computable.mixin', 'approval.mixin']

    name = fields.Char(string='Name', required=True)
    roll_number = fields.Char(string='Roll Number')


class ClassBStudent(models.Model):
    _name = 'class_b.student'
    _description = 'Class B Student'
    _inherit = ['grade.computable.mixin', 'approval.mixin']
    name = fields.Char(string='Name', required=True)
    roll_number = fields.Char(string='Roll Number')


class ClassCStudent(models.Model):
    _name = 'class_c.student'
    _description = 'Class C Student'
    _inherit = ['grade.computable.mixin', 'approval.mixin']
    name = fields.Char(string='Name', required=True)
    roll_number = fields.Char(string='Roll Number')

# class StudentStatusMixin(models.AbstractModel):
#     _name = 'student.status.mixin'
#     _description = 'Mixin for Student Academic Status'
#
#     status = fields.Selection([
#         ('enrolled', 'Enrolled'),
#         ('passed', 'Passed'),
#         ('failed', 'Failed'),
#         ('dropped', 'Dropped Out'),
#     ], string='Academic Status', default='enrolled', required=True)
#
#     status_note = fields.Text(string='Status Note')
#
#     def mark_passed(self):
#         for record in self:
#             record.status = 'passed'
#             record.status_note = "Student passed successfully."
#
#     def mark_dropped(self):
#         for record in self:
#             record.status = 'dropped'
#             record.status_note = "Student has dropped out."
