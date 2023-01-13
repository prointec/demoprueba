odoo.define('hr_dashboard_app_ent.Dashboard',function(require){
"use strict";

var AbstractAction = require('web.AbstractAction');
var ajax = require('web.ajax');
var core = require('web.core');
var Dialog = require('web.Dialog');
var field_utils = require('web.field_utils');
var session = require('web.session');
var web_client = require('web.web_client');
var Widget = require('web.Widget');
var rpc = require('web.rpc');

var _t = core._t;
var QWeb = core.qweb;

var Dashboard = AbstractAction.extend({
	hasControlPanel: true,
	contentTemplate: 'hr_dashboard_app_ent.Dashboard',

	events: {
		'click .column': 'on_click_list',
		'click .form_view' : 'on_click_form',
		'change #BirthDate' : 'on_change_date',
	},

	init: function(parent, context) {
		this._super(parent, context);
		this.dashboard_stage_templates = ['hr_dashboard_app_ent.dashboard_view'];
		this.dashboard_birthday_templates = ['hr_dashboard_app_ent.birthday_list'];
	},
	willStart: function() {
		var self = this;
		return $.when(ajax.loadLibs(this), this._super()).then(function() {
			return self.fetch_data();
		})
	},

	start: function() {
		var self = this;
		self.render_dashboards();
		return this._super();
	},

	fetch_data: function() {
		var self = this;
		var prom = this._rpc({
			route: '/hr/fetch_dashboard_data',
		});
		prom.then(function(result) {
			self.user = result['user'];
			self.leave_total = result['leaves_total'];
			self.leaves_count = result['leaves_count'];
			self.birthday = result['birthday'];
			self.announcement = result['announcement'];
			self.count = result['count'];
			self.payslip = result['payslip'];
			self.expense = result['expense'];
			self.attendance = result['attendance'];
			self.leaves = result['leaves'];
		});
		return prom;
	},

	render_dashboards: function() {
		var self = this;
		_.each(this.dashboard_stage_templates, function(template) {
			self.$('.o_dashboard_stage').append(QWeb.render(template, {widget: self}));  
		});
		this.$('.datepicker').datepicker({
			clearBtn: true,
			format: "dd/mm/yyyy"
		});
	},
	
	on_click_list: function (ev){
		var self = this;
		var model_name = $(ev.currentTarget).find('.name').text();
		var model = '';
		var name = '';
		var user = session.uid
		var model_view = '';
		if (model_name == 'Expenses'){
			name = 'Expenses';
			model = 'hr.expense';
			model_view = 'hr_expense.view_expenses_tree';
		}
		if (model_name == 'Leaves'){
			name = 'Leaves';
			model = 'hr.leave';
			model_view = 'hr_holidays.hr_leave_view_tree_my';
		}
		if (model_name == 'Payslip'){
			name = 'Payslip';
			model = 'hr.payslip';
			model_view = 'hr_payroll.view_hr_payslip_tree';
		}
		if (model_name == 'Contracts'){
			name = 'Contracts';
			model = 'hr.contract';
			model_view = 'hr_contract.hr_contract_view_tree';
		}
		if (model_name == 'Attendance'){
			name = 'Attendance';
			model = 'hr.attendance';
			model_view = 'hr_attendance.view_attendance_tree';
		}
		self.do_action({
			name: name,
			views: [[false, 'list'], [false, 'form']],
			res_model: model,
			domain: [["employee_id.user_id", "=", user]],
			type: 'ir.actions.act_window',
			target: 'current',
		});
	},


	on_click_form: function(ev){
		var self = this;
		var model_name = $(ev.currentTarget).prev().prev().text();
		var model = '';
		var name = '';
		var model_view = '';
		if (model_name == 'Expenses'){
			name = 'Expenses'
			model = 'hr.expense'
			model_view = 'hr_expense.hr_expense_view_form'
		}
		if (model_name == 'Leaves'){
			name = 'Leaves'
			model = 'hr.leave'
			model_view = 'hr_holidays.hr_leave_view_form'
		}
		if (model_name == 'Payslips'){
			name = 'Payslip'
			model = 'hr.payslip'
			model_view = 'hr_payroll.view_hr_payslip_form'
		}
		if (model_name == 'Contracts'){
			name = 'Contracts'
			model = 'hr.contract'
			model_view = 'hr_contract.hr_contract_view_form'
		}
		if (model_name == 'Attendance'){
			name = 'Attendance'
			model = 'hr.attendance'
			model_view = 'hr_attendance.hr_attendance_view_form'
		}
		self.do_action({
			name: name,
			views: [[false, 'form']],
			res_model: model,
			type: 'ir.actions.act_window',
			target: 'current',
		});
	},

	on_change_date: function(ev){
		var self = this;
		this._rpc({
			route: '/hr/fetch_birthdate_data',
			params: {data : ev.currentTarget.value}
		}).then(function(result) {
			self.birthday = result['birthday'];
			self.$('.birth_list').remove();
			_.each(self.dashboard_birthday_templates, function(template) {
				self.$('.birthday_list').append(QWeb.render(template, {widget: self}));  
			});
		});
	},
});

core.action_registry.add('hr_dashboard', Dashboard);

return Dashboard;
});