frappe.listview_settings['Recruitment Agencies'] = {

	get_indicator: function (doc) {
		if (doc.status === "Enable") {
			return [__("Enable"), "green", "status,=,Enable"];
		} else if (doc.status === "Disable") {
			return [__("Disable"), "red", "status,=,Disable"];
		} else {
			return [__("Cancelled"), "red", "status,=,Cancelled"];
		}
	}
};
