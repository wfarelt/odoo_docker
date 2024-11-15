# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Student(models.Model):
    _name = 'school.student'
    _description = 'Student'

    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age')
    grade = fields.Selection([
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('higher', 'Higher'),
    ], string='Grade', required=True)
    tutor_id = fields.Many2one('school.tutor', string='Tutor', ondelete='set null')
    course_id = fields.Many2one('school.course', string='Course', ondelete='set null')
    
    user_id = fields.Many2one('res.users', string="Odoo User", help="Related Odoo user for student")
    
    @api.model
    def create(self, vals):
        # Crear el estudiante
        student = super(Student, self).create(vals)

        # Crear el usuario en Odoo vinculado al estudiante sin grupos y con una contraseña predeterminada
        user_vals = {
            'name': student.name,
            'login': student.name.lower().replace(" ", "") + "@school.com",  # Generar un email de ejemplo
            'password': 'user123*',  # Contraseña predeterminada
            'groups_id': [(6, 0, [self.env.ref('base.group_user').id])],
        }
        
        # Crear el usuario
        user = self.env['res.users'].sudo().create(user_vals)
        
        # Vincular el usuario creado con el estudiante
        student.user_id = user.id
        
        return student
    
class Tutor(models.Model):
    _name = 'school.tutor'
    _description = 'Tutor'

    name = fields.Char(string='Name', required=True)
    contact_info = fields.Char(string='Contact Information')
    student_ids = fields.One2many('school.student', 'tutor_id', string='Students')

class Teacher(models.Model):
    _name = 'school.teacher'
    _description = 'Teacher'

    name = fields.Char(string='Name', required=True)
    contact_info = fields.Char(string='Contact Information')
    course_ids = fields.One2many('school.course', 'teacher_id', string='Courses')
    
    # Campo para relacionar un usuario de Odoo
    user_id = fields.Many2one('res.users', string="Odoo User", help="Related Odoo user for teacher")
    

class Course(models.Model):
    _name = 'school.course'
    _description = 'Course'

    # Nombre del curso, por ejemplo, "Matemáticas I", Cantidad de alumnos, Profesor, etc.
    name = fields.Char(string='Name', required=True)
    student_count = fields.Integer(string='Student Count', default=20)
    teacher_id = fields.Many2one('school.teacher', string='Teacher', ondelete='set null')
    student_ids = fields.One2many('school.student', 'course_id', string='Students')

  
class Assignment(models.Model):
    _name = 'school.assignment'
    _description = 'Assignment'

    name = fields.Char(string="Assignment Name", required=True)
    description = fields.Text(string="Description")
    due_date = fields.Date(string="Due Date", default=fields.Date.today)
    course_id = fields.Many2one('school.course', string="Course", ondelete='set null')
    student_ids = fields.Many2many('school.student', 'course_id',string="Students")
    teacher_id = fields.Many2one('school.teacher', string="Teacher", related='course_id.teacher_id', store=True)

    @api.onchange('course_id')
    def _onchange_course_id(self):
        if self.course_id:
            self.student_ids = [(6, 0, self.course_id.student_ids.ids)]

class Submission(models.Model):
    _name = 'school.submission'
    _description = 'Student Submission for Assignments'

    student_id = fields.Many2one('school.student', string="Student", readonly=True)
    teacher_id = fields.Many2one('school.teacher', string="Teacher", related='assignment_id.teacher_id', readonly=True)
    assignment_id = fields.Many2one('school.assignment', string="Assignment")
    submission_date = fields.Datetime(string="Submission Date", default=fields.Datetime.now)
    file_url = fields.Char(string="File URL")
    grade = fields.Float(string="Grade")
    feedback = fields.Text(string="Feedback")  
    
    @api.model
    def create(self, vals):
        # Obtener el usuario logueado
        current_user = self.env.user
        # Buscar el estudiante relacionado con este usuario
        student = self.env['school.student'].search([('user_id', '=', current_user.id)], limit=1)
        if student:
            vals['student_id'] = student.id
        else:
            raise ValidationError("No está asociado a ningún estudiante.")
        return super(Submission, self).create(vals)
    
        
        