// Client Script for Actividad Comercial
// Copyright (c) 2024, SBC Internationals

frappe.ui.form.on('Actividad Comercial', {
	refresh: function(frm) {
		// Add custom buttons
		if (!frm.is_new()) {
			add_custom_buttons(frm);
		}
		
		// Set field properties
		set_field_properties(frm);
		
		// Add status indicator
		add_status_indicator(frm);
		
		// Auto-refresh calendar if open
		if (frm.doc.fecha_hora) {
			update_calendar_view(frm);
		}
	},
	
	fecha_hora: function(frm) {
		calculate_end_time(frm);
	},
	
	duracion_minutos: function(frm) {
		calculate_end_time(frm);
	},
	
	tipo_actividad: function(frm) {
		// Show/hide ubicacion section
		set_ubicacion_visibility(frm);
	},
	
	estado: function(frm) {
		handle_estado_change(frm);
		add_status_indicator(frm);
	},
	
	cliente: function(frm) {
		// Auto-fill employee from client if not set
		if (frm.doc.cliente && !frm.doc.empleado_responsable) {
			frappe.db.get_value('Cliente Turistico', frm.doc.cliente, 'empleado_asignado', (r) => {
				if (r.empleado_asignado) {
					frm.set_value('empleado_responsable', r.empleado_asignado);
				}
			});
		}
	},
	
	ubicacion: function(frm) {
		// Show video call link if virtual
		toggle_videocall_field(frm);
	},
	
	crear_seguimiento: function(frm) {
		// Set default follow-up date
		if (frm.doc.crear_seguimiento && !frm.doc.fecha_seguimiento) {
			let followup_date = frappe.datetime.add_days(frm.doc.fecha_hora, 7);
			frm.set_value('fecha_seguimiento', followup_date);
		}
	}
});

// Helper Functions

function calculate_end_time(frm) {
	if (frm.doc.fecha_hora && frm.doc.duracion_minutos) {
		let start = frappe.datetime.str_to_obj(frm.doc.fecha_hora);
		let end = new Date(start.getTime() + frm.doc.duracion_minutos * 60000);
		frm.set_value('fecha_fin', frappe.datetime.obj_to_str(end));
	}
}

function set_ubicacion_visibility(frm) {
	let show_ubicacion = ['Reunión', 'Visita Cliente', 'Evento Asistido'].includes(frm.doc.tipo_actividad);
	frm.toggle_display('seccion_ubicacion', show_ubicacion);
}

function toggle_videocall_field(frm) {
	let show_link = frm.doc.ubicacion === 'Virtual' || frm.doc.ubicacion === 'Online';
	frm.toggle_display('enlace_videollamada', show_link);
}

function handle_estado_change(frm) {
	// Show result section when completed
	frm.toggle_display('seccion_resultado', frm.doc.estado === 'Completada');
	
	// Set completion time
	if (frm.doc.estado === 'Completada' && !frm.doc.__islocal) {
		if (!frm.doc.resultado) {
			frm.scroll_to_field('resultado');
			frappe.msgprint({
				title: __('Actividad Completada'),
				indicator: 'green',
				message: __('Por favor ingrese el resultado de la actividad')
			});
		}
	}
}

function add_custom_buttons(frm) {
	// Quick mark as completed
	if (frm.doc.estado !== 'Completada' && frm.doc.estado !== 'Cancelada') {
		frm.add_custom_button(__('Marcar Completada'), function() {
			frm.set_value('estado', 'Completada');
			frm.save();
		}, __('Acciones'));
	}
	
	// Create follow-up activity
	if (frm.doc.estado === 'Completada') {
		frm.add_custom_button(__('Crear Seguimiento'), function() {
			create_followup_activity(frm);
		}, __('Acciones'));
	}
	
	// View related reservation
	if (frm.doc.reserva_relacionada) {
		frm.add_custom_button(__('Ver Reserva'), function() {
			frappe.set_route('Form', 'Reserva Paquete', frm.doc.reserva_relacionada);
		}, __('Ver'));
	}
	
	// View client
	if (frm.doc.cliente) {
		frm.add_custom_button(__('Ver Cliente'), function() {
			frappe.set_route('Form', 'Cliente Turistico', frm.doc.cliente);
		}, __('Ver'));
	}
	
	// Send email reminder
	if (frm.doc.estado === 'Programada') {
		frm.add_custom_button(__('Enviar Recordatorio'), function() {
			send_reminder_email(frm);
		}, __('Acciones'));
	}
	
	// Add to calendar
	frm.add_custom_button(__('Agregar a Calendario'), function() {
		add_to_google_calendar(frm);
	}, __('Acciones'));
}

function set_field_properties(frm) {
	// Make title required and bold
	frm.fields_dict.titulo.$wrapper.addClass('font-weight-bold');
	
	// Color code priority
	if (frm.doc.prioridad) {
		let priority_colors = {
			'Urgente': 'red',
			'Alta': 'orange',
			'Media': 'blue',
			'Baja': 'gray'
		};
		// Could add visual indicator here
	}
}

function add_status_indicator(frm) {
	let color_map = {
		'Programada': 'blue',
		'En Curso': 'orange',
		'Completada': 'green',
		'Cancelada': 'red',
		'Pospuesta': 'gray'
	};
	
	frm.page.set_indicator(frm.doc.estado, color_map[frm.doc.estado]);
}

function create_followup_activity(frm) {
	frappe.prompt([
		{
			label: 'Fecha de Seguimiento',
			fieldname: 'fecha',
			fieldtype: 'Date',
			default: frappe.datetime.add_days(frappe.datetime.now_date(), 7),
			reqd: 1
		},
		{
			label: 'Tipo de Actividad',
			fieldname: 'tipo',
			fieldtype: 'Select',
			options: 'Seguimiento\nLlamada Comercial\nReunión\nEmail',
			default: 'Seguimiento',
			reqd: 1
		},
		{
			label: 'Notas',
			fieldname: 'notas',
			fieldtype: 'Small Text'
		}
	], function(values) {
		frappe.call({
			method: 'frappe.client.insert',
			args: {
				doc: {
					doctype: 'Actividad Comercial',
					titulo: `Seguimiento: ${frm.doc.titulo}`,
					tipo_actividad: values.tipo,
					estado: 'Programada',
					prioridad: frm.doc.prioridad,
					cliente: frm.doc.cliente,
					reserva_relacionada: frm.doc.reserva_relacionada,
					empleado_responsable: frm.doc.empleado_responsable,
					fecha_hora: `${values.fecha} 09:00:00`,
					duracion_minutos: 30,
					descripcion: `<p>Seguimiento de: ${frm.doc.name}</p><p>${values.notas || ''}</p>`
				}
			},
			callback: function(r) {
				if (r.message) {
					frappe.msgprint({
						title: __('Seguimiento Creado'),
						indicator: 'green',
						message: __(`Actividad ${r.message.name} creada exitosamente`)
					});
					frappe.set_route('Form', 'Actividad Comercial', r.message.name);
				}
			}
		});
	}, __('Crear Actividad de Seguimiento'), __('Crear'));
}

function send_reminder_email(frm) {
	frappe.call({
		method: 'frappe.core.doctype.communication.email.make',
		args: {
			recipients: frm.doc.empleado_responsable,
			subject: `Recordatorio: ${frm.doc.titulo}`,
			content: get_reminder_template(frm),
			send_email: 1
		},
		callback: function(r) {
			frappe.msgprint({
				title: __('Email Enviado'),
				indicator: 'green',
				message: __('Recordatorio enviado exitosamente')
			});
		}
	});
}

function get_reminder_template(frm) {
	return `
		<h3>Recordatorio de Actividad</h3>
		<p><strong>Actividad:</strong> ${frm.doc.titulo}</p>
		<p><strong>Tipo:</strong> ${frm.doc.tipo_actividad}</p>
		<p><strong>Fecha y Hora:</strong> ${frm.doc.fecha_hora}</p>
		<p><strong>Duración:</strong> ${frm.doc.duracion_minutos} minutos</p>
		${frm.doc.cliente ? `<p><strong>Cliente:</strong> ${frm.doc.cliente}</p>` : ''}
		${frm.doc.ubicacion ? `<p><strong>Ubicación:</strong> ${frm.doc.ubicacion}</p>` : ''}
		${frm.doc.enlace_videollamada ? `<p><strong>Enlace:</strong> <a href="${frm.doc.enlace_videollamada}">${frm.doc.enlace_videollamada}</a></p>` : ''}
		<hr>
		<p>${frm.doc.descripcion || ''}</p>
	`;
}

function add_to_google_calendar(frm) {
	if (!frm.doc.fecha_hora) {
		frappe.msgprint(__('Por favor establezca una fecha y hora primero'));
		return;
	}
	
	let start_time = frappe.datetime.str_to_obj(frm.doc.fecha_hora);
	let end_time = frm.doc.fecha_fin ? frappe.datetime.str_to_obj(frm.doc.fecha_fin) : 
		new Date(start_time.getTime() + 60 * 60000); // Default 1 hour
	
	let calendar_url = `https://calendar.google.com/calendar/render?action=TEMPLATE` +
		`&text=${encodeURIComponent(frm.doc.titulo)}` +
		`&dates=${format_google_date(start_time)}/${format_google_date(end_time)}` +
		`&details=${encodeURIComponent(frm.doc.descripcion || '')}` +
		`&location=${encodeURIComponent(frm.doc.ubicacion || '')}`;
	
	window.open(calendar_url, '_blank');
}

function format_google_date(date) {
	// Format: YYYYMMDDTHHmmSSZ
	return date.toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';
}

function update_calendar_view(frm) {
	// Trigger calendar refresh if calendar view is open
	if (cur_list && cur_list.doctype === 'Actividad Comercial' && cur_list.view_name === 'Calendar') {
		cur_list.refresh();
	}
}
