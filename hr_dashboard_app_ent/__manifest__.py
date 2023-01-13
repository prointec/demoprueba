# -*- coding: utf-8 -*-

{
    'name' : 'HR Dashboard - Enterprise Edition',
    'author': "Edge Technologies",
    'version' : '14.0.1.0',
    'live_test_url':'https://youtu.be/DIIYuJoLNT0',
    "images":['static/description/main_screenshot.png'],
    'summary' : 'Human Resource Dashboard for HR dashboard expense dashboard employee dashboard payslip dashboard leave dashboard contract Dashboard recruitment dashboard attendance Dashboard  Attractive HR Dashboard all in one hr dashboard payroll dashboard',
    'description' : """
        HR Dashboard app helps to view information of employee.
     """,
    "license" : "OPL-1",
    'depends': ['base','sale_management','hr_expense','hr_recruitment','hr_holidays','hr','account','project','hr_attendance', 'hr_payroll'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',

    ],
    'qweb' : [
        "static/src/xml/dashboard.xml",
    ],
    'installable' : True,
    'auto_install' : False,
    'price': 15,
    'currency': "EUR",
    'category' : 'Human Resources',
}
