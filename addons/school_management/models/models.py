# -*- coding: utf-8 -*-

from odoo import models, fields, api

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

class Course(models.Model):
    _name = 'school.course'
    _description = 'Course'

    # Nombre del curso, por ejemplo, "Matemáticas I", Cantidad de alumnos, Profesor, etc.
    name = fields.Char(string='Name', required=True)
    student_count = fields.Integer(string='Student Count')
    teacher_id = fields.Many2one('school.tutor', string='Teacher', ondelete='set null')
    student_ids = fields.Many2many('school.student', string='Students')
    
    
    
    
