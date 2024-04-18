frappe.listview_settings['Recruitment'] = {
	get_indicator: function (doc) {
		if (doc.status === "Open") {
			return [__("Open"), "orange", "status,=,Open"];
		} else if (doc.status === "Declined") {
			return [__("Declined"), "red", "status,=,Declined"];
		} else if (doc.status === "Schedule Assignment") {
			return [__("Schedule Assignment"), "yellow", "status,=,Schedule Assignment"];
		} else if (doc.status === "Hired") {
			return [__("Hired"), "red", "status,=,Hired"];
		}
	}
};
