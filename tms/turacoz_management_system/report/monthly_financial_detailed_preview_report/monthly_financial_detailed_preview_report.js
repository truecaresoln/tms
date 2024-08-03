// Copyright (c) 2024, RSA and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Monthly Financial Detailed Preview Report"] = {
	"filters": [
		{
			"fieldname":"key",
			"label": __("Category"),
			"fieldtype": "Select",
			"options": ["","total_unraised_amount_till_date","actual_invoice_raised_mtd","actual_invoice_raised_ytd","payment_received_mtd","payment_received_ytd","planned_invoices_to_be_raised_in_week","planned_invoices_to_be_raised_mtd","payment_to_be_received_mtd","payment_to_be_received_ytd"],
			"hidden":1,
			"reqd": 0
		}

	]
};
