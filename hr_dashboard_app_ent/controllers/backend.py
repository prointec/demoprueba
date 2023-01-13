from odoo import http
from odoo.http import request
from odoo import api, fields, models, _, tools
from datetime import datetime, date
from odoo.exceptions import UserError, ValidationError
import pytz
from dateutil import tz

class HelpdeskBackend(http.Controller):

	@http.route('/hr/fetch_dashboard_data', type="json", auth='user')
	def fetch_dashboard_data(self):
		
		user_id = request.env.user.id
		dashboard_data = {}
		now = datetime.now()
		employee = request.env['hr.employee'].sudo()
		announcement = request.env['hr.announcement'].sudo()
		attendance = request.env['hr.attendance'].sudo()
		expense = request.env['hr.expense'].sudo()
		leaves = request.env['hr.leave'].sudo()
		payslip = request.env['hr.payslip'].sudo()
		contract = request.env['hr.contract'].sudo()
		data = {}
		birthdate_data = {}
		for datas in employee.search([]):
			if datas.birthday:
				if datas.birthday.day <= now.date().day and datas.birthday.month <= now.date().month:
					birthdate_data[datas.id] = datas.name
		dashboard_data['birthday'] = birthdate_data

		announcement_data = {}
		for datas in announcement.search([]):
			announcement_data[str(datas.announcement_date)] = datas.name
		dashboard_data['announcement'] = announcement_data

		leave_count = {}
		leave_count['pending'] = leaves.search_count([('employee_id.name','=', request.env.user.name),('state','=','confirm')])
		leave_count['approved'] = leaves.search_count([('employee_id.name','=', request.env.user.name),('state','=','validate')])
		leave_count['cancelled'] = leaves.search_count([('employee_id.name','=', request.env.user.name),('state','=','cancel')])
		leave_count['refused'] = leaves.search_count([('employee_id.name','=', request.env.user.name),('state','=','refuse')])

		total_leave = {}

		approved_leave = 0.0
		allocated_leave = 0.0
		if request.env.user.has_group('base.user_admin'):
			leaves_id = request.env['hr.leave.allocation'].search([])
		else:
			leaves_id = request.env['hr.leave.allocation'].search([('employee_id.name','=', request.env.user.name)])

		for leave in leaves_id:
			if (leave.state == 'validate'):
				if leave.type_request_unit != 'hour':
					approved_leave += leave.number_of_days_display
			if leave.type_request_unit != 'hour':
					allocated_leave += leave.number_of_days_display

		total_leave['leave_approved'] = approved_leave
		total_leave['leave_allocated'] = allocated_leave
		
		payslip_vals = {}
		for pay in payslip.search([('employee_id.name','=', request.env.user.name)]):
			pay_slip = {}
			pay_slip['number'] = pay.number if pay.number else '' 
			pay_slip['date_from'] = pay.date_from
			pay_slip['date_to'] = pay.date_to
			pay_slip['state'] = dict(pay._fields['state'].selection).get(pay.state)
			payslip_vals[pay.id] = pay_slip

		expenses_vals = {}
		for expenses in expense.search([('employee_id.name','=', request.env.user.name)]):
			expense_dict = {}
			expense_dict['date'] = expenses.date
			expense_dict['name'] = expenses.name
			expense_dict['total'] = expenses.total_amount
			expense_dict['state'] = dict(expenses._fields['state'].selection).get(expenses.state)
			expenses_vals[expenses.id] = expense_dict

		attendance_vals = {}

		for attendances in attendance.search([('employee_id.name','=', request.env.user.name)]):
			attendance_dict = {}

			user_tz = pytz.timezone(request.env.context.get('tz') or request.env.user.tz or 'UTC')
			check_in_time = pytz.UTC.localize(fields.Datetime.from_string(attendances.check_in))
			check_in = check_in_time.astimezone(user_tz)

			if attendances.check_out:
				check_out_time = pytz.UTC.localize(fields.Datetime.from_string(attendances.check_out))
				check_out = check_out_time.astimezone(user_tz)

			attendance_dict['date'] = attendances.check_in.date() if attendances.check_in else ''
			attendance_dict['check_in'] = check_in.time() if attendances.check_in else ''
			attendance_dict['check_out'] = check_out.time() if attendances.check_out else '' 
			attendance_vals[attendances.id] = attendance_dict

		leaves_vals = {}
		for leaves in leaves.search([('employee_name.name','=', request.env.user.name)]):
			leave_dict = {}
			leave_dict['request_out'] = leaves.request_date_from
			leave_dict['request_in'] = leaves.request_date_to
			leave_dict['leave_type'] = leaves.holiday_status_id.name
			leave_dict['state'] = dict(leaves._fields['state'].selection).get(leaves.state)
			leaves_vals[leaves.id] = leave_dict
		count = {}
		count['payslip'] = payslip.search_count([('employee_id.name','=', request.env.user.name)])

		count['attendance'] = attendance.search_count([('employee_id.name','=', request.env.user.name)])
		total = 0.0
		for data in expense.search([('employee_id.name','=', request.env.user.name)]):     
			total += data.total_amount

		count['contract'] = contract.search_count([('employee_id.name','=', request.env.user.name)])
		count['expense'] = '{0:.2f}'.format(total)
		dashboard_data['user'] = request.env.user.name
		dashboard_data['leaves_total'] = total_leave
		dashboard_data['leaves_count'] = leave_count
		dashboard_data['count'] = count
		dashboard_data['payslip'] = payslip_vals
		dashboard_data['expense'] = expenses_vals
		dashboard_data['attendance'] = attendance_vals
		dashboard_data['leaves'] = leaves_vals

		return dashboard_data

	@http.route('/hr/fetch_birthdate_data', type="json", auth='user')
	def fetch_birthday_data(self, data):
		dashboard_data = {}
		# now = datetime.now()
		try:
			datetime.strptime(data, '%d/%m/%Y')
		except ValueError:
			raise UserError(_("Incorrect data format"))
		date_time_obj = datetime.strptime(data, '%d/%m/%Y')
		employee = request.env['hr.employee']
		birthdate_data = {}
		for datas in employee.search([]):	
			if datas.birthday:
				if datas.birthday.day == date_time_obj.date().day and datas.birthday.month == date_time_obj.date().month:
					birthdate_data[datas.id] = datas.name
		dashboard_data['birthday'] = birthdate_data

		return dashboard_data
		