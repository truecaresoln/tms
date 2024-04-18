// Copyright (c) 2023, RSA and contributors
// For license information, please see license.txt

frappe.ui.form.on('Hourly Calculation', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('Hourly Calculation Details', {
	"effort_hour": function(frm, cdt, cdn) {
		let gridRow = frm.open_grid_row();
		if (!gridRow) {
			gridRow = frm.get_field('hourly_details').grid.get_row(cdn);
		}
		calAmount(gridRow);
	},
	"rate_per_hour": function(frm, cdt, cdn) {
		let gridRow = frm.open_grid_row();
		if (!gridRow) {
			gridRow = frm.get_field('hourly_details').grid.get_row(cdn);
		}
		calAmount(gridRow);
	},
	
});

function calAmount(gridRow) {
	let effort_hour = gridRow.on_grid_fields_dict.effort_hour.value;
	let rate_per_hour = gridRow.on_grid_fields_dict.rate_per_hour.value;
	let total_amount = effort_hour * rate_per_hour;
	frappe.model.set_value(
		gridRow.doc.doctype,
		gridRow.doc.name,
		'amount_to_be_paid',
		total_amount
		);
}
