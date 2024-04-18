// Copyright (c) 2021, RSA and contributors
// For license information, please see license.txt

frappe.ui.form.on('Internal Project Feedback', {
	refresh: function(frm) {
		frm.set_value("date", frappe.datetime.get_today());
	},

	onload: function(frm){
		var employee = frm.doc.employee;
		if (frm.is_new()) {
			var userid =  frappe.session.user;
			frm.set_value("user", userid);
		}

		cur_frm.set_query("employee", function() {
			return {
				"filters": {
			    	"enabled": ("=", 1)
			   }
			};
		});
	},

	template: function(frm){
		var tem = frm.doc.template;
		frappe.call({
			"method": "frappe.client.get",
			args: {
				doctype: "Internal Feedback Template",
				name: frm.doc.template
			},
			callback: function(data){
				frm.fields_dict.parameters.grid.remove_all();
				for (var i in data.message.internal_feedback_parameters){
					frm.add_child("parameters");
					frm.fields_dict.parameters.get_value()[i].parameter = data.message.internal_feedback_parameters[i].parameter;
				}
				frm.refresh();
			}
		});
		
	}
});

frappe.ui.form.on("Internal Project Feedback Parameter", {
    "value": function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        var total_score = 0;
        frm.doc.parameters.forEach(function(d) { total_score += parseInt(d.value); });
	var total_score_value = total_score / 11;
	var fnts = total_score_value .toFixed(2);
        frm.set_value('total_score', fnts);
    },
	/*"reviewer": function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		var total_reviewer = 0;
		frm.doc.parameters.forEach(function(d) { total_reviewer += parseInt(d.reviewer); });
		var total_score_reviewer = total_reviewer / 11;
		var fnr = total_score_reviewer.toFixed(2);
		frm.set_value('total_score_reviewer', fnr);
	 },	
	
	"qcer": function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		var total_qcer = 0;
		frm.doc.parameters.forEach(function(d) { total_qcer += parseInt(d.qcer); });
		var total_score_qcer = total_qcer / 11;
		var fnq = total_score_qcer.toFixed(2);
		frm.set_value('total_score_qcer', fnq);
	 },

	"designer": function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		var total_designer = 0;
		frm.doc.parameters.forEach(function(d) { total_designer += parseInt(d.designer); });
		var total_score_designer = total_designer / 11;
		var fnd = total_score_designer.toFixed(2);
		frm.set_value('total_score_designer', fnd);
	 },
	
	"project_manager": function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		var total_project_manager = 0;
		frm.doc.parameters.forEach(function(d) { total_project_manager += parseInt(d.project_manager); });
		var total_score_project_manager = total_project_manager / 11;
		var fnm = total_score_project_manager.toFixed(2);
		frm.set_value('total_score_project_manager', fnm);
	 },*/
	/*"qty": function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        var total = 0;
        frm.doc.invoice_particulars.forEach(function(d) { total += d.amount; });
        frm.set_value('net_total', total);
	var total_taxes = frm.doc.total_taxes;
	var rounded_total = total+total_taxes;
	frm.set_value('grand_total',rounded_total);
    },*/	
});
