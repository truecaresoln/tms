frappe.listview_settings['My Task Allocation'] = {

	get_indicator: function (doc) {
		if (doc.status === "Open") {
			return [__("Open"), "red", "status,=,Open"];
		} else if (doc.status === "Cancelled") {
			return [__("Cancelled"), "red", "status,=,Cancelled"];
		} else if (doc.status === "On Hold") {
			return [__("On Hold"), "orange", "status,=,On Hold"];
		} else if (doc.status === "Close") {
			return [__("Close"), "green", "status,=,Close"];
		} else {
			return [__("Overdue"), "red", "status,=,Overdue"];
		}
	}
};
