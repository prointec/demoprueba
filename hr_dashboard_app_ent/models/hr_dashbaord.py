# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime,date                               
from odoo.exceptions import UserError, ValidationError

class HrDashboard(models.Model):
	_name = 'hr.dashboard'
	
	name=fields.Char(string="Name")

	@api.model
	def action_dashboard_redirect(self):
		return self.env["ir.actions.actions"]._for_xml_id('hr_dashboard_app_ent.hr_dashboard')

class HrAnnouncement(models.Model):
	_name = 'hr.announcement'
	
	name=fields.Text(string="Announcement")
	announcement_date=fields.Date(string="Date")
	sequence=fields.Integer(string="Sequence")
	active = fields.Boolean(default=True, help="Set active to false to hide.")

class HrLeave(models.Model):
	_inherit = 'hr.leave'

	employee_name=fields.Many2one('res.users',string="Employee",default=lambda self: self.env.user.id)