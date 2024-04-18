// Copyright (c) 2023, RSA and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["DMS"] = {
	"filters": [
		{
			"fieldname":"session",
			"label": __("Session"),
			"fieldtype": "Select",
			"options": ['2014-15','2015-16','2016-17','2017-18','2018-19','2019-20','2020-21','2021-22','2022-23','2023-24','2024-25'],
			"reqd": 0
			
		},		
		{
			"fieldname": "search_string",
			"label": __("Search"),
			"fieldtype": "Data",
			"reqd": 0
		},
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"reqd": 0
		},
		{
			"fieldname":"dtype",
			"label": __("Document Type"),
			"fieldtype": "Link",
			"options": "DMS Document Type",
			"reqd": 0
		},
		{
			"fieldname":"department",
			"label": __("Department"),
			"fieldtype": "Link",
			"options": "DMS Department",
			"reqd": 0
		},
		{
			"fieldname":"category",
			"label": __("Category"),
			"fieldtype": "Link",
			"options": "DMS Category",
			"reqd": 0,
			get_query: () => {
				var department1 = frappe.query_report.get_filter_value('department');
				return {
					filters: {
						'department': department1
					}
				}
			}
		},
		{
			"fieldname":"sub_category",
			"label": __("Sub Category"),
			"fieldtype": "Link",
			"options": "DMS Sub Category",
			"reqd": 0,
			get_query: () => {
				var category1 = frappe.query_report.get_filter_value('category');
				return {
					filters: {
						'category': category1
					}
				}
			}
		},
		{
			"fieldname":"project_code",
			"label": __("Project Code"),
			"fieldtype": "Link",
			"options": "Project",
			"reqd": 0
		},

	],
};
