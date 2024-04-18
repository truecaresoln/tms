frappe.listview_settings['Approvals'] = {
	onload: function(listview) {
			frappe.route_options = {
//				"owner": ["=",frappe.session.user],
				"status": ["=", "Draft"]
			};
	},

	get_indicator: function (doc) {
		if (doc.status === "Approved") {
			return [__("Approved"), "green", "status,=,Approved"];
		} else if (doc.status === "Rejected") {
			return [__("Rejected"), "red", "status,=,Rejected"];
		} else if (doc.status === "Approved by Accountant") {
			return [__("Approved"), "green", "status,=,Approved"];
		} else if (doc.status === "Approved by Reporting Manager") {
			return [__("Approved"), "green", "status,=,Approved"];
		} else {
			return [__("Draft"), "red", "status,=,Draft"];
		}
	}
};
