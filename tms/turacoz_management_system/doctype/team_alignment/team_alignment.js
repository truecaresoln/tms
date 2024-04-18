// Copyright (c) 2021, RSA and contributors
// For license information, please see license.txt

frappe.ui.form.on('Team Alignment', {

	 onload: function(frm) {
		
		/*User Filter Here*/
		var user_id = frappe.session.user;
		const options = {name: user_id};
		const fields = ['is_all_employee_access'];
		frappe.db.get_value('Financially Active', options, fields).then(({ message }) => {
			if (message) {
				//frm.set_value("project_title", message.project_title);
				if(message.is_all_employee_access==0){
					frm.fields_dict.team_detail.grid.get_field("allocated_to").get_query = function(doc){
			
					       return {
						   query:"tms.turacoz_management_system.doctype.team_alignment.team_alignment.setUser"
					       }

					}
				}
				
			}
		});
		
		var task = frm.doc.task;
		if(task){
			frm.toggle_display("team_detail",true);
			frm.toggle_display("align_freelancer",true);
		}else{
			frm.toggle_display("team_detail",false);
			frm.toggle_display("align_freelancer",false);
		}
				
		if(frm.is_new()){
			var user_id = frappe.session.user;
			var task = frm.doc.task;
			if(task){
				set_record_section_hide_show(frm,task);
			}
			if(user_id){
				frm.set_value("assigned_by", user_id);
			}
			
			var project = frm.doc.project;
			
			if(project){
				set_dms_link(frm,project);
			}
		}

		set_task_filter(frm);

		/*Freelancer Active Filter Here*/
		cur_frm.fields_dict["align_freelancer"].grid.get_field("freelancer").get_query = function(doc){		
		       return {
			       filters:{
					"status" : "Active"
			       }
		       }
		}

		var is_viatris_project = frm.doc.is_viatris_project;
		if(is_viatris_project == "No"){
			frm.set_df_property("pud_technical_input", "reqd", 1);
		}
		else{
			frm.set_df_property("pud_technical_input", "reqd", 0);
		}

		
		var project = frm.doc.project;
		cur_frm.set_query("pud_technical_input", function() {
			return {
				"filters": {
			    	"project": ("=", project)
			   }
			};
		});

	 },
	 "task": function(frm){
	 	var task = frm.doc.task;
		if(task){
			frm.toggle_display("team_detail",true);
			frm.toggle_display("align_freelancer",true);
		}else{
			frm.toggle_display("team_detail",false);
			frm.toggle_display("align_freelancer",false);
		}
	 },

	"project":function(frm){

		set_task_filter(frm);
	},
	
	"is_viatris_project":function(frm){
		var is_viatris_project = frm.doc.is_viatris_project;
		if(is_viatris_project == "No"){
			frm.set_df_property("pud_technical_input", "reqd", 1);
		}
		else{
			frm.set_df_property("pud_technical_input", "reqd", 0);
		}
	},
	
});

// function filter for task 
const set_task_filter = function(frm){
	var project = frm.doc.project;
		cur_frm.set_query("task", function() {
			return {
				"filters": {
			    	"project": ("=", project)
			   }
			};
		});
}
	
// set information of task
const set_record_section_hide_show = function(frm,task) {
	let today = new Date().toISOString().slice(0, 10);

	const options = {name: task};
	const fields = ['subject'];
	frappe.db.get_value('Task', options, fields).then(({ message }) => {
		if (message) {
			frm.set_value("task_description", message.subject);
			frm.set_value("reference_type", 'Task');
			frm.set_value("reference_name", task);
		}
	});

};

//set dms link
const set_dms_link = function(frm,project){
	const options = {name: project};
	const fields = ['dms_project_link'];
	frappe.db.get_value('Project', options, fields).then(({ message }) => {
		if (message) {
			frm.set_value("dms_project_link", message.dms_project_link);
		}
	});
};

// set information of project type
const set_pud_hide_when_projecttype_internal = function(frm,project) {
	const options = {name: project};
	const fields = ['project_type'];
	frappe.db.get_value('Project', options, fields).then(({ message }) => {
		if (message) {
			if(message.project_type=="External")
			{
				frm.set_df_property("pud_technical_input", "reqd", 1);
			}
			else
			{
				frm.set_df_property("pud_technical_input", "reqd", 0);
			}
		}
	});

};

// Set ToDo name via Team Alignment 
frappe.ui.form.on('Team Alignment Employee', {
	"allocated_to": function(frm, cdt, cdn) {
		let gridRow = frm.open_grid_row();
		if (!gridRow) {
			gridRow = frm.get_field('team_detail').grid.get_row(cdn);
		}
		callTodoName(gridRow);
	},
	"role": function(frm, cdt, cdn) {
		let gridRow = frm.open_grid_row();
		if (!gridRow) {
			gridRow = frm.get_field('team_detail').grid.get_row(cdn);
		}
		callTodoName(gridRow);
	},
	"description": function(frm, cdt, cdn) {
		let gridRow = frm.open_grid_row();
		if (!gridRow) {
			gridRow = frm.get_field('team_detail').grid.get_row(cdn);
		}
		callTodoName(gridRow);
	},
	"allocated_hours": function(frm, cdt, cdn) {
		let gridRow = frm.open_grid_row();
		if (!gridRow) {
			gridRow = frm.get_field('team_detail').grid.get_row(cdn);
		}
		var d = locals[cdt][cdn];
		var total = 0;
		frm.doc.team_detail.forEach(function(d) { total += d.allocated_hours; });
		checkRemainingAllocatedHours(gridRow,frm,total);
	},
	
	
});

function callTodoName(gridRow,frm) {
	let allocated_to = gridRow.on_grid_fields_dict.allocated_to.value;
	let role = gridRow.on_grid_fields_dict.role.value;
	let description = gridRow.on_grid_fields_dict.description.value;
	let project = cur_frm.doc.project;
	let task = cur_frm.doc.task;
	let name_str = description+' - '+project+' - '+task+' - '+role+' - '+allocated_to;
	frappe.model.set_value(
		gridRow.doc.doctype,
		gridRow.doc.name,
		'todo_name',
		name_str
		);

}

//set freelancer child name
frappe.ui.form.on('Align Freelancer', {
	"freelancer": function(frm, cdt, cdn) {
		let gridRow = frm.open_grid_row();
		if (!gridRow) {
			gridRow = frm.get_field('align_freelancer').grid.get_row(cdn);
		}
		callFreelancerName(gridRow);
	},
	"role": function(frm, cdt, cdn) {
		let gridRow = frm.open_grid_row();
		if (!gridRow) {
			gridRow = frm.get_field('align_freelancer').grid.get_row(cdn);
		}
		callFreelancerName(gridRow);
	},
	"type_of_document": function(frm, cdt, cdn) {
		let gridRow = frm.open_grid_row();
		if (!gridRow) {
			gridRow = frm.get_field('align_freelancer').grid.get_row(cdn);
		}
		callFreelancerName(gridRow);
	},
	
	
});

function callFreelancerName(gridRow,frm) {
	let freelancer = gridRow.on_grid_fields_dict.freelancer.value;
	let role = gridRow.on_grid_fields_dict.role.value;
	let type_of_document = gridRow.on_grid_fields_dict.type_of_document.value;
	let project = cur_frm.doc.project;
	let task = cur_frm.doc.task;
	
	let name_str = project+'-'+task+'-'+role+'-'+freelancer+'-'+type_of_document;
	frappe.model.set_value(
		gridRow.doc.doctype,
		gridRow.doc.name,
		'freelancer_project_detail_name',
		name_str
		);

}


//function to check remaining Allocated hours
function checkRemainingAllocatedHours(gridRow,frm,total_alloc_hrs) {
//	let allocated_hours = gridRow.on_grid_fields_dict.allocated_hours.value;
	let task = cur_frm.doc.task;
	frappe.call({
        	method: "tms.turacoz_management_system.doctype.team_alignment.team_alignment.getprojecthours",
		args:{ "task":task,"allocated_hours":total_alloc_hrs
		},
		callback:function(res){
			let a = res.message;
			if (a==0){
				frappe.msgprint("Total hours allocated to task is more than remaining hours");
				frappe.model.set_value(
					gridRow.doc.doctype,
					gridRow.doc.name,
					'allocated_hours',
					''					
					);
			}
		}
        })
}


//dynamic buttons
frappe.ui.form.on("Team Alignment", "refresh", function(frm) 
{
	var project = frm.doc.project;
	if(frm.doc.project!=undefined)
	{
		frappe.call({
			"method": "frappe.client.get",
			 args: {
				doctype: "Challenges and Commitments",
				name: "CHALLENGE-2021-Internal-8524"
			},
			callback: function (data) {
				frm.add_custom_button(__('Get Challenges'), function(){ 
					challenge();
				});
			}
		})
	} 

	if(frm.doc.project!=undefined)
	{
		frappe.call({
			"method": "frappe.client.get",
			 args: {
				doctype: "Challenges and Commitments",
				name: "CHALLENGE-2021-Internal-8524"
			},
			callback: function (data) {
				frm.add_custom_button(__('Get Project Updates'), function(){ 
					getUpdate();
				});
			}
		})
	}

	if(frm.doc.project!=undefined)
	{
		frappe.call({
			"method": "frappe.client.get",
			 args: {
				doctype: "Challenges and Commitments",
				name: "CHALLENGE-2021-Internal-8524"
			},
			callback: function (data) {
				frm.add_custom_button(__('Get Proposed Dates'), function(){ 
					getProposedDate();
				});
			}
		})
	}

});


//code for get content from data base and set it into child table
/*frappe.ui.form.on("Team Alignment", "onload", function(frm,doctype,name) {
	  var project = cur_frm.doc.project;
	   frappe.call({
	     method: 'frappe.client.get_list',
	     args: {
	       doctype: 'Challenges and Commitments',
	       columns: ['name','date'],
	       filters:{
			'project':cur_frm.doc.project, 
		},
	       fields:["name","description_of_challenge","date"] 
	     },
	     callback: function(res){
		for(var i=0; i< res.message.length; i++){
			var new_row = cur_frm.add_child("challenges_and_commitments")
			new_row.description_of_challenge=res.message[i].description_of_challenge;
			new_row.challenges_and_commitments = res.message[i].name;
			new_row.date = res.message[i].date;
			cur_frm.refresh_fields("challenges_and_commitments");
				
		
		}
	     }
	   })
});*/

//frappe.ui.form.on('Team Alignment', 'onload', function(frm, cdt, cdn){
//});

// get content from database and set it into message view through custom button
function challenge(){
	
   var project = cur_frm.doc.project;
   frappe.call({
     method: 'frappe.client.get_list',
     args: {
       doctype: 'Challenges and Commitments',
       columns: ['name','date'],
       filters:{
		'project':cur_frm.doc.project, 
	},
       fields:["name","description_of_challenge","date"] 
     },
     callback: function(res){
	cur_frm.clear_table("challenges_and_commitments")
	var html= '<table class="table" id="test"><th>Name</th><th>Description</th><th>Date</th>';
	var body="";
	var footer="</table>"
	for(var i=0; i< res.message.length; i++){
		/*var new_row = cur_frm.add_child("challenges_and_commitments")
		new_row.description_of_challenge=res.message[i].description_of_challenge;
		new_row.challenges_and_commitments = res.message[i].name;
		new_row.date = res.message[i].date;
		cur_frm.refresh_fields("challenges_and_commitments");*/
	
		body+='<tr><td>'+res.message[i].name+'</td>'+'<td>'+res.message[i].description_of_challenge+'</td>'+'<td>'+res.message[i].date+'</td></tr>'
		
	
	}
	var final = html+body+footer;
	//frappe.msgprint(final)
	// with options
	frappe.msgprint({
	    title: __('Challenges'),
	    indicator: 'green',
	    message: __(final)
	});
     }
   })
}

//get Update
function getUpdate(frm) {  
	frappe.call({
        	method: "tms.turacoz_management_system.doctype.team_alignment.team_alignment.getprojectUpdates",
		args:{ "project":cur_frm.doc.project
		},
		callback:function(res){
			var html= '<table class="table" id="test"><th>Deliverable</th><th>Deliverable Type</th><th>Client Sent Date</th>';
			var body="";
			var footer="</table>"
			for(var i=0; i< res.message.length; i++){
			
				body+='<tr><td>'+res.message[i].module+'</td>'+'<td>'+res.message[i].deliverable+'</td>'+'<td>'+res.message[i].client_sent_date+'</td></tr>'
			}
			var final = html+body+footer;
			frappe.msgprint({
			    title: __('Project Updates'),
			    indicator: 'green',
			    message: __(final)
			});
		}
        })	
        
}

//get project proposed dates
function getProposedDate(){
	frappe.call({
        	method: "tms.turacoz_management_system.doctype.team_alignment.team_alignment.getprojectProposed",
		args:{ "project":cur_frm.doc.project
		},
		callback:function(res){
			var html= '<table class="table" id="test"><th>Deliverable</th><th>Deliverable Type</th><th>Proposed Start Date</th><th>Proposed End Date</th>';
			var body="";
			var footer="</table>"
			for(var i=0; i< res.message.length; i++){
			
				body+='<tr><td>'+res.message[i].module+'</td>'+'<td>'+res.message[i].deliverable+'</td>'+'<td>'+res.message[i].proposed_date+'</td>'+'<td>'+res.message[i].proposed_end_date+'</td>'+'</tr>'
			}
			var final = html+body+footer;
			frappe.msgprint({
			    title: __('Project Proposed Deliverable'),
			    indicator: 'red',
			    message: __(final)
			});
		}
        })
}

//get project Updates
function getProjectUpdates(){
	
  var project = cur_frm.doc.project;
   frappe.call({
     method: 'frappe.client.get_list',
     args: {
       doctype: 'Project Update Data',
       columns: ['name','date'],
       filters:{
		'parent':cur_frm.doc.project, 
	},
       fields:["module","deliverable","client_sent_date"] 
     },
     callback: function(res){
	var html= '<table class="table" id="test"><th>Deliverable</th><th>Deliverable Type</th><th>Client Sent Date</th>';
	var body="";
	var footer="</table>"
	for(var i=0; i< res.message.length; i++){
	
		body+='<tr><td>'+res.message[i].name+'</td>'+'<td>'+res.message[i].description_of_challenge+'</td>'+'<td>'+res.message[i].date+'</td></tr>'
		
	
	}
	var final = html+body+footer;
	//frappe.msgprint(final)
	// with options
	frappe.msgprint({
	    title: __('Project Updates'),
	    indicator: 'green',
	    message: __(final)
	});
     }
   })
}




