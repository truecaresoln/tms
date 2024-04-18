# Copyright (c) 2013, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe import _
import frappe
from datetime import datetime
from datetime import timedelta
import calendar
import pendulum
import datetime

def execute(filters=None):
	columns, data = [], []
	return columns, data

def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_data(filters):
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	data = []
	
	return data

def get_columns(filters):
	cols = []
	cols=[
		{
			"fieldname": "name",
			"label": ("Name"),
			"fieldtype": "Data",
			"width": "150",
			"hidden": "true"
		},
	]
	
	return cols	
