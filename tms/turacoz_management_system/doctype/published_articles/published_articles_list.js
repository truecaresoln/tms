// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

// render
frappe.listview_settings['Published Articles'] = {
	add_fields: ["name", "project", "therapeutic_area", "article_status"],
	get_indicator: function(doc) {
		const status_colors = {
			"Draft": "grey",
			"Submitted": "orange",
			"In Submission": "orange",
			"In Acceptance": "blue",
			"Published": "green",
			"Rejected": "red"
		};
		return [__(doc.article_status), status_colors[doc.article_status], "status,=,"+doc.article_status];
	},
	right_column: "project_manager"
};
