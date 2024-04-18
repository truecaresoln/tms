// Copyright (c) 2021, RSA and contributors
// For license information, please see license.txt

frappe.ui.form.on('Student Invoice', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('Student Invoice Particular', {
	"qty": function(frm, cdt, cdn) {
		let gridRow = frm.open_grid_row();
		if (!gridRow) {
			gridRow = frm.get_field('particular').grid.get_row(cdn);
		}
		calAmount(gridRow);
	},
	"rate": function(frm, cdt, cdn) {
		let gridRow = frm.open_grid_row();
		if (!gridRow) {
			gridRow = frm.get_field('particular').grid.get_row(cdn);
		}
		calAmount(gridRow);
	},
	
});

function calAmount(gridRow) {
	let qty = gridRow.on_grid_fields_dict.qty.value;
	let rate = gridRow.on_grid_fields_dict.rate.value;
	let amount = qty * rate;
	frappe.model.set_value(
		gridRow.doc.doctype,
		gridRow.doc.name,
		'amount',
		amount
		);
}

frappe.ui.form.on("Student Invoice Particular", {
    "rate": function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        var total = 0;
        frm.doc.particular.forEach(function(d) { total += d.amount; });
        frm.set_value('net_total', total);
	var total_taxes = frm.doc.total_taxes;
	var rounded_total = total+total_taxes;
	frm.set_value('grand_total',rounded_total);
    },
	
	"qty": function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        var total = 0;
        frm.doc.particular.forEach(function(d) { total += d.amount; });
        frm.set_value('net_total', total);
	var total_taxes = frm.doc.total_taxes;
	var rounded_total = total+total_taxes;
	frm.set_value('grand_total',rounded_total);
    },	
});

frappe.ui.form.on('Custom Invoice Taxes', {
	"tax_rate": function(frm, cdt, cdn) {
		let gridRow = frm.open_grid_row();
		if (!gridRow) {
			gridRow = frm.get_field('tax_calculation').grid.get_row(cdn);
		}
		calTax(gridRow);
	},
});

function calTax(gridRow) {
	let taxname = gridRow.on_grid_fields_dict.tax_name.value;
	let taxrate = gridRow.on_grid_fields_dict.tax_rate.value;
	let taxAmount = gridRow.on_grid_fields_dict.tax_amount.value;
	let netTotal = cur_frm.doc.net_total;
	let taxamount = netTotal*taxrate/100;
	
	frappe.model.set_value(
		gridRow.doc.doctype,
		gridRow.doc.name,
		'tax_amount',
		taxamount
		);
	if(taxname=='IGST')
	{
		cur_frm.set_value('igst',taxamount);
	}
	else if(taxname=='CGST')
	{
		cur_frm.set_value('cgst',taxamount);
	}
	else if(taxname=='SGST')
	{
		cur_frm.set_value('sgst',taxamount);
	}
}

frappe.ui.form.on("Custom Invoice Taxes", {
    "tax_rate": function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        var total = 0;
        frm.doc.tax_calculation.forEach(function(d) { total += d.tax_amount; });
        frm.set_value('total_taxes', total);
	var net_total = frm.doc.net_total;
	var grand_total = 0;
	grand_total = total+net_total;
	frm.set_value('grand_total',grand_total);
    },	
});


