// Copyright (c) 2021, RSA and contributors
// For license information, please see license.txt
frappe.ui.form.on('Project Detail Template', {
	onload: function(frm) {
		var company = frm.doc.company;
		if(company == 'Turacoz Healthcare Solutions Pvt Ltd')
		{
			frm.set_value('company_short_name','THS');
		}
		else if(company == 'Turacoz Solutions LLC')
		{
			frm.set_value('company_short_name','TSLLC');
		}
		else if(company == 'Turacoz Solutions PTE Ltd.')
		{
			frm.set_value('company_short_name','TSPL');
		}
		else if(company == 'Turacoz B.V.')
		{
			frm.set_value('company_short_name','TBV');
		}
		else if(company == 'Turacoz Canada Inc')
		{
			frm.set_value('company_short_name','TCI');
		}

		var user_id = frappe.session.user;
		if(user_id){
			set_record_section_hide_show(frm,user_id);
		}
		if(frm.is_new()){
			frm.set_value("project",'');
		}

		cur_frm.set_query("bank_account", function() {
			return {
				"filters": {
			    	"company": ("=", company)
			   }
			};
		});

		//project manager Filter
		cur_frm.set_query("project_manager", function() {
			return {
				"filters": {
			    	"department": ["in", ["Project Management - THS","Business Development - THS"]]
			    }
			};
		});
		
		//Team Leader Filter
		cur_frm.set_query("team_lead_medical_writer", function() {
			return {
				"filters": {
			    	"department": ("=", "Medical Services - THS")
			    }
			};
		});
		
		//BD Person Filter
		cur_frm.set_query("bd_person", function() {
			return {
				"filters": {
			    	"department": ["in", ["Project Management - THS","Business Development - THS"]]
			    }
			};
		});
		
		cur_frm.set_query("contact_person", function(){
            	if(frm.doc.customer) {
                	return {
                    		query: "frappe.contacts.doctype.contact.contact.contact_query",
                    		filters: { link_doctype: "Customer", link_name: cur_frm.doc.customer }
                		};
          		}
        	});

		var hours = frm.doc.hours;
		
		if(hours){
			frm.toggle_display("hours", false);
		}
		
		
		/*var a = "Business Development - THS";
		cur_frm.set_query("bd_person", function() {
			return {
				"filters": {
			    	"department" : ("=", a)
			   }
			};
		});*/

		//bd filters
		
					
			
	},

	
	"popcd_status":function(frm){
		var popcd_status = frm.doc.popcd_status;
		if(popcd_status == "Received"){
			frm.set_df_property("po_pcd_attachment", "reqd", 1);
		}
		else{
			frm.set_df_property("po_pcd_attachment", "reqd", 0);
		}	
	},

	"source_document":function(frm){
		var source_document = frm.doc.source_document;
		if(source_document == "Pending"){
			frm.set_df_property("source_document_attachment", "reqd", 0);
		}
		else if(source_document == "NA"){
			frm.set_df_property("source_document_attachment", "reqd", 0);
		}
		else{
			frm.set_df_property("source_document_attachment", "reqd", 1);
		}	
	},

	"client_brief":function(frm){
		var client_brief = frm.doc.client_brief;
		if(client_brief == "Pending"){
			frm.set_df_property("client_brief_attachment", "reqd", 0);
		}
		else if(client_brief == "NA"){
			frm.set_df_property("client_brief_attachment", "reqd", 0);
		}
		else{
			frm.set_df_property("client_brief_attachment", "reqd", 1);
		}	
	},

	"vendor_registration_form":function(frm){
		var vendor_registration_form = frm.doc.vendor_registration_form;
		if(vendor_registration_form == "Not Attached"){
			frm.set_df_property("vendor_registration_attachment", "reqd", 0);
		}
		else if(vendor_registration_form == "NA"){
			frm.set_df_property("vendor_registration_attachment", "reqd", 0);
		}
		else{
			frm.set_df_property("vendor_registration_attachment", "reqd", 1);
		}	
	},

	"service_agreement":function(frm){
		var service_agreement = frm.doc.service_agreement;
		if(service_agreement == "Pending"){
			frm.set_df_property("service_agreement_attachment", "reqd", 0);
		}
		else if(service_agreement == "NA"){
			frm.set_df_property("service_agreement_attachment", "reqd", 0);
		}
		else{
			frm.set_df_property("service_agreement_attachment", "reqd", 1);
		}	
	},

	"cda":function(frm){
		var cda = frm.doc.cda;
		if(cda == "Pending"){
			frm.set_df_property("cda_attachment", "reqd", 0);
		}
		else if(cda == "NA"){
			frm.set_df_property("cda_attachment", "reqd", 0);
		}
		else{
			frm.set_df_property("cda_attachment", "reqd", 1);
		}	
	},

	"final_rfp":function(frm){
		var final_rfp = frm.doc.final_rfp;
		if(final_rfp == "Not Attached"){
			frm.set_df_property("final_rfp_attachment", "reqd", 0);
		}
		else if(final_rfp == "NA"){
			frm.set_df_property("final_rfp_attachment", "reqd", 0);
		}
		else{
			frm.set_df_property("final_rfp_attachment", "reqd", 1);
		}	
	},

	"client_communication_mail":function(frm){
		var client_communication_mail = frm.doc.client_communication_mail;
		if(client_communication_mail == "Not Attached"){
			frm.set_df_property("client_communication_attachment", "reqd", 0);
		}
		else if(client_communication_mail == "NA"){
			frm.set_df_property("client_communication_attachment", "reqd", 0);
		}
		else{
			frm.set_df_property("client_communication_attachment", "reqd", 1);
		}	
	},

	"call_recordings_if_any":function(frm){
		var call_recordings_if_any = frm.doc.call_recordings_if_any;
		if(call_recordings_if_any == "Not Attached"){
			frm.set_df_property("call_recording_attachment", "reqd", 0);
		}
		else if(call_recordings_if_any == "NA"){
			frm.set_df_property("call_recording_attachment", "reqd", 0);
		}
		else{
			frm.set_df_property("call_recording_attachment", "reqd", 1);
		}	
	},

	"services":function(frm)
	{
		var service = frm.doc.services;
		
		cur_frm.set_query("service_type", function() {
			return {
				"filters": {
			    	"service": ("=", service)
			   }
			};
		});
	},
	
	"hours":function(frm)
	{
		var hours = frm.doc.hours;
		
		if(hours>70)
		{
			frm.set_value('actual_client_hours',(hours/2));
			frm.set_value('profitability_hours',(hours/2));
		}
		else
		{
			frm.set_value('actual_client_hours',hours);
			frm.set_value('profitability_hours',0);
		}
		
		var total_planned_hours_25_per = hours-(hours*25/100);
		var fn_hrs = total_planned_hours_25_per.toFixed(2);
		frm.set_value('total_planned_hours', fn_hrs);
		
	},
	
	"pms_ongoing_project_list": function(frm){
		var userid = frappe.session.user;
		frappe.call({
			method: "tms.turacoz_management_system.doctype.project_detail_template.project_detail_template.get_pms_detail",
			args:{ "userid":userid
			},
			callback:function(res){
				var html= '<table class="table" id="test"><th>PM Name</th><th>Total Ongoing Projects</th>';
				var body="";
				var footer="</table>"
				for(var i=0; i< res.message.length; i++){
				
					body+='<tr><td>'+res.message[i].employee_name+'</td>'+'<td>'+res.message[i].projects_count+'</td></tr>'
				}
				var final = html+body+footer;
				frappe.msgprint({
				    title: __('PM Suggestion'),
				    indicator: 'green',
				    message: __(final)
				});
			}
		})
	},

	"company":function(frm){

		var company = frm.doc.company;
		if(company == 'Turacoz Healthcare Solutions Pvt Ltd')
		{
			frm.set_value('company_short_name','THS');
		}
		else if(company == 'Turacoz Solutions LLC')
		{
			frm.set_value('company_short_name','TSLLC');
		}
		else if(company == 'Turacoz Solutions PTE Ltd.')
		{
			frm.set_value('company_short_name','TSPL');
		}
		else if(company == 'Turacoz B.V.')
		{
			frm.set_value('company_short_name','TBV');
		}
		else if(company == 'Turacoz Canada Inc')
		{
			frm.set_value('company_short_name','TCI');
		}

		cur_frm.set_query("bank_account", function() {
			return {
				"filters": {
			    	"company": ("=", company)
			   }
			};
		});

		/*cur_frm.set_query("bd_person", function() {
			return {
				"filters": {
			    	"department" : a
			   }
			};
		});*/
	}
});

/*frappe.ui.form.on("Project Detail Template", "refresh", function(frm) { 
	if(frm.doc.docstatus==1){
		frappe.call({//may i see the wait.. i will see the location can you direct me to
        		method: "tms.turacoz_management_system.doctype.project_detail_template.project_detail_template.datasample",
			callback:function(r){
				frappe.msgprint("hello")
			}// can you direct me to the py file? try direct me ag
        	})	
         // msgprint("Welcome Update Event");
	}
});*/



// set information hide and show section
const set_record_section_hide_show = function(frm,user_id) {
	//let today = new Date().toISOString().slice(0, 10);
	//let role = 'Technical Project Head';

	const options = {user: user_id};
	const fields = ['is_financially_active','is_pm_allocator','is_teamlead_allocator','total_planned_hour','budgeted_hour'];
	frappe.db.get_value('Financially Active', options, fields).then(({ message }) => {
		if (message) {
			//frm.set_value("project_title", message.project_title);
			if(message.is_financially_active==0){
				frm.toggle_display("project_cost_and_payment_detail_section", false);
				frm.toggle_display("project_manager_and_team_lead_medical_writer_alignment_section", true);
			}
			else
			{
				frm.toggle_display("project_cost_and_payment_detail_section", true);
				frm.toggle_display("project_manager_and_team_lead_medical_writer_alignment_section", true);
			}
			
			if(message.is_pm_allocator==1)
			{
				frm.set_df_property("project_manager", "reqd", 1);
				frm.toggle_display("project_manager", true);
				
				frm.set_df_property("team_lead_medical_writer", "reqd", 0);
				frm.toggle_display("team_lead_medical_writer", true);
				
				frm.toggle_display("total_planned_hours",true); 
				frm.set_df_property("total_planned_hours", "reqd", 1);
				frm.toggle_display("hours",true); 
				
			}
			
			if(message.is_teamlead_allocator==1)
			{
				
				frm.set_df_property("team_lead_medical_writer", "reqd", 1);
				frm.toggle_display("team_lead_medical_writer", true);
				
				
				frm.set_df_property("project_manager", "read_only", 1);
				
				frm.toggle_display("total_planned_hours",true);
				frm.set_df_property("total_planned_hours", "read_only", 1);
			}
			
			if(message.total_planned_hour==1)
			{
				frm.toggle_display("total_planned_hours",true);
				frm.set_df_property("total_planned_hours", "reqd", 1);
			}
		}
	});

};



