# -*- coding: utf-8 -*-

from odoo import models, fields, api

class task(models.Model):
    _name = 'manage.task'
    _description = 'manage.task'

    name = fields.Char(string="Task Name", required=True)
    
# class manage(models.Model):
#     _name = 'manage.manage'
#     _description = 'manage.manage'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
