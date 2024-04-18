// Copyright (c) 2021, RSA and contributors
// For license information, please see license.txt

frappe.ui.form.on('Recruitment', {

	 onload: function(frm) {

		frm.set_query('recruitment_agency_name', function(){
			return {
				filters : [
					['status', '=', 'Enable']
				]
			};
		});		

		var recruitment_agency_name = frm.doc.recruitment_agency_name;
		if(recruitment_agency_name){
			frm.toggle_display("recruitment_agency_name", true);
		}
		else{
			frm.toggle_display("recruitment_agency_name", false);
		}

		var job_portals_name = frm.doc.job_portals_name;
		if(job_portals_name){
			frm.toggle_display("job_portals_name", true);
		}
		else{
			frm.toggle_display("job_portals_name", false);
		}

		var internal_reference_name = frm.doc.internal_reference_name;
		if(internal_reference_name){
			frm.toggle_display("internal_reference_name", true);
		}
		else{
			frm.toggle_display("internal_reference_name", false);
		}

		var relevant_experience = frm.doc.relevant_experience;
		if(relevant_experience){
			frm.toggle_display("relevant_experience",true);
		}
		else{
			frm.toggle_display("relevant_experience",false);
		}

		var total_exprience = frm.doc.total_exprience;
		if(total_exprience){
			frm.toggle_display("total_exprience",true);
		}
		else{
			frm.toggle_display("total_exprience",false);
		}

		var variable_amount = frm.doc.variable_amount;
		if(variable_amount){
			frm.toggle_display("variable_amount",true);
		}
		else{
			frm.toggle_display("variable_amount",false);
		}

		var amount = frm.doc.amount;
		if(amount == ""){
		}
		else{
		}
	 },

	 refresh: function(frm) {
		if(frm.is_new()){
			frm.toggle_display("job_portals_name", false);
			frm.toggle_display("internal_reference_name", false);
			frm.toggle_display("recruitment_agency_name", false);
			frm.toggle_display("relevant_experience",false);
			frm.toggle_display("total_exprience",false);
			frm.toggle_display("variable_amount",false);
			frm.toggle_display("amount",false);
		}
	 },

	 "variable_amount":function(frm){
		var variable_amount = frm.doc.variable_amount;
		var var_amount = 0;
		if(variable_amount){
			var_amount = variable_amount;
		}
		else{
			var_amount = 0;
		}
		var amount = frm.doc.amount;
		var fx_amount = 0;
		if(amount){
			fx_amount = amount;
		}
		else{
			fx_amount = 0;
		}
		var total_ctc = var_amount + fx_amount;
		frm.set_value("total_ctc_amount", total_ctc);
	 },

	 "ectc_percentage":function(frm){
		var ectc_percentage = frm.doc.ectc_percentage;
		var total_ctc_amount = frm.doc.total_ctc_amount;
		var total_after_percentage = total_ctc_amount + total_ctc_amount*ectc_percentage/100;
		frm.set_value("ectc", total_after_percentage);
	 },
	
	 "amount":function(frm){
		var variable_amount = frm.doc.variable_amount;
		var var_amount = 0;
		if(variable_amount){
			var_amount = variable_amount;
		}
		else{
			var_amount = 0;
		}
		var amount = frm.doc.amount;
		var fx_amount = 0;
		if(amount){
			fx_amount = amount;
		}
		else{
			fx_amount = 0;
		}
		var total_ctc = var_amount + fx_amount;
		frm.set_value("total_ctc_amount", total_ctc);
	 },

	 "ctc":function(frm){
		var ctc = frm.doc.ctc;
		if(ctc == "Variable and Fixed"){
			frm.set_value("variable_amount", '');
			frm.set_value("amount", '');
			frm.toggle_display("variable_amount",true);
			frm.set_df_property("variable_amount", "reqd", 1);
			frm.toggle_display("amount",true);
			frm.set_df_property("amount", "reqd", 1);
		}
		else{
			frm.set_value("variable_amount", '');
			frm.set_value("amount", '');
			frm.toggle_display("variable_amount",false);
			frm.set_df_property("variable_amount", "reqd", 0);
			frm.toggle_display("amount",true);
			frm.set_df_property("amount", "reqd", 1);
		}
	 },

	 "experience":function(frm){
		var experience = frm.doc.experience;
		if(experience == "Yes"){
			frm.set_df_property("ctc", "reqd", 1);
			frm.toggle_display("relevant_experience",true);
			frm.set_df_property("relevant_experience", "reqd", 1);
			frm.toggle_display("total_exprience",true);
			frm.set_df_property("total_exprience", "reqd", 1);
		}
		else{
			frm.set_df_property("ctc", "reqd", 0);
			frm.toggle_display("relevant_experience",false);
			frm.set_df_property("relevant_experience", "reqd", 0);
			frm.toggle_display("total_exprience",false);
			frm.set_df_property("total_exprience", "reqd", 0);
		}
	 },

	"source":function(frm){
		var source = frm.doc.source;
		if(source == "Recruitment Agency"){
			frm.toggle_display("recruitment_agency_name", true);
			frm.set_df_property("recruitment_agency_name", "reqd", 1);
			frm.toggle_display("job_portals_name", false);
			frm.set_df_property("job_portals_name", "reqd", 0);
			frm.toggle_display("internal_reference_name", false);
			frm.set_df_property("internal_reference_name", "reqd", 0);
		}
		else if(source == "Internal Reference"){
			frm.toggle_display("recruitment_agency_name", false);
			frm.set_df_property("recruitment_agency_name", "reqd", 0);
			frm.toggle_display("job_portals_name", false);
			frm.set_df_property("job_portals_name", "reqd", 0);
			frm.toggle_display("internal_reference_name", true);
			frm.set_df_property("internal_reference_name", "reqd", 1);
		}
		else if(source == "Job Portals"){
			frm.toggle_display("recruitment_agency_name", false);
			frm.set_df_property("recruitment_agency_name", "reqd", 0);
			frm.toggle_display("job_portals_name", true);
			frm.set_df_property("job_portals_name", "reqd", 1);
			frm.toggle_display("internal_reference_name", false);
			frm.set_df_property("internal_reference_name", "reqd", 0);
		}
		else{
			frm.toggle_display("recruitment_agency_name", false);
			frm.set_df_property("recruitment_agency_name", "reqd", 0);
			frm.toggle_display("job_portals_name", false);
			frm.set_df_property("job_portals_name", "reqd", 0);
			frm.toggle_display("internal_reference_name", false);
			frm.set_df_property("internal_reference_name", "reqd", 0);
		}
	},
});
