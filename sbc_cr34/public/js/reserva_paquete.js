// Client Script for Reserva Paquete
// Copyright (c) 2024, SBC Internationals

frappe.ui.form.on('Reserva Paquete', {
	refresh: function(frm) {
		// Add custom buttons
		if (!frm.is_new()) {
			add_custom_buttons(frm);
		}
		
		// Set field properties
		set_field_properties(frm);
		
		// Add color indicators
		add_status_indicator(frm);
	},
	
	cliente: function(frm) {
		// Auto-fill fields from client
		if (frm.doc.cliente) {
			frappe.call({
				method: 'sbc_cr34.sbc_crm.doctype.reserva_paquete.reserva_paquete.get_client_info',
				args: {
					client: frm.doc.cliente
				},
				callback: function(r) {
					if (r.message) {
						frm.set_value('porcentaje_comision', r.message.porcentaje_comision);
						if (!frm.doc.empleado_responsable) {
							frm.set_value('empleado_responsable', r.message.empleado_responsable);
						}
						if (!frm.doc.nacionalidad_grupo) {
							frm.set_value('nacionalidad_grupo', r.message.nacionalidad_grupo);
						}
					}
				}
			});
		}
	},
	
	fecha_inicio: function(frm) {
		calculate_nights(frm);
	},
	
	fecha_fin: function(frm) {
		calculate_nights(frm);
	},
	
	num_adultos: function(frm) {
		calculate_total_persons(frm);
	},
	
	num_ninos: function(frm) {
		calculate_total_persons(frm);
	},
	
	num_bebes: function(frm) {
		calculate_total_persons(frm);
	},
	
	valor_paquete_base: function(frm) {
		calculate_totals(frm);
	},
	
	descuento_porcentaje: function(frm) {
		calculate_totals(frm);
	},
	
	porcentaje_comision: function(frm) {
		calculate_commission(frm);
	},
	
	estado: function(frm) {
		add_status_indicator(frm);
	}
});

// Child table: Servicio Adicional Reserva
frappe.ui.form.on('Servicio Adicional Reserva', {
	cantidad: function(frm, cdt, cdn) {
		calculate_service_total(frm, cdt, cdn);
	},
	
	precio_unitario: function(frm, cdt, cdn) {
		calculate_service_total(frm, cdt, cdn);
	},
	
	servicios_adicionales_add: function(frm) {
		frm.refresh_field('servicios_adicionales');
	},
	
	servicios_adicionales_remove: function(frm) {
		calculate_totals(frm);
	}
});

// Helper Functions

function calculate_nights(frm) {
	if (frm.doc.fecha_inicio && frm.doc.fecha_fin) {
		let start = frappe.datetime.str_to_obj(frm.doc.fecha_inicio);
		let end = frappe.datetime.str_to_obj(frm.doc.fecha_fin);
		let diff = frappe.datetime.get_day_diff(end, start);
		
		if (diff >= 0) {
			frm.set_value('num_noches', diff);
		}
	}
}

function calculate_total_persons(frm) {
	let total = (frm.doc.num_adultos || 0) + 
				(frm.doc.num_ninos || 0) + 
				(frm.doc.num_bebes || 0);
	frm.set_value('num_personas_total', total);
}

function calculate_service_total(frm, cdt, cdn) {
	let row = locals[cdt][cdn];
	let total = (row.cantidad || 0) * (row.precio_unitario || 0);
	frappe.model.set_value(cdt, cdn, 'total', total);
	
	// Recalculate main totals
	setTimeout(() => {
		calculate_totals(frm);
	}, 100);
}

function calculate_totals(frm) {
	// Calculate additional services total
	let services_total = 0;
	if (frm.doc.servicios_adicionales) {
		frm.doc.servicios_adicionales.forEach(function(service) {
			services_total += (service.total || 0);
		});
	}
	frm.set_value('valor_servicios_adicionales', services_total);
	
	// Calculate subtotal
	let subtotal = (frm.doc.valor_paquete_base || 0) + services_total;
	
	// Calculate discount
	let discount = subtotal * (frm.doc.descuento_porcentaje || 0) / 100;
	frm.set_value('descuento_monto', discount);
	
	// Calculate total
	let total = subtotal - discount;
	frm.set_value('valor_total', total);
	
	// Calculate commission
	calculate_commission(frm);
}

function calculate_commission(frm) {
	if (frm.doc.valor_total && frm.doc.porcentaje_comision) {
		let commission = frm.doc.valor_total * frm.doc.porcentaje_comision / 100;
		frm.set_value('comision_sbc', commission);
	}
}

function add_custom_buttons(frm) {
	// Duplicate button
	frm.add_custom_button(__('Duplicar Reserva'), function() {
		frappe.call({
			method: 'sbc_cr34.sbc_crm.doctype.reserva_paquete.reserva_paquete.duplicate_reservation',
			args: {
				source_name: frm.doc.name
			},
			callback: function(r) {
				if (r.message) {
					frappe.set_route('Form', 'Reserva Paquete', r.message.name);
				}
			}
		});
	});
	
	// Email button
	if (frm.doc.cliente) {
		frm.add_custom_button(__('Enviar Email'), function() {
			frappe.call({
				method: 'frappe.core.doctype.communication.email.make',
				args: {
					recipients: frm.doc.cliente,
					subject: `Reserva ${frm.doc.name} - ${frm.doc.titulo_reserva}`,
					content: get_email_template(frm)
				}
			});
		});
	}
	
	// Create activity button
	frm.add_custom_button(__('Crear Actividad'), function() {
		frappe.new_doc('Actividad Comercial', {
			cliente: frm.doc.cliente,
			reserva_relacionada: frm.doc.name,
			empleado_responsable: frm.doc.empleado_responsable
		});
	});
}

function set_field_properties(frm) {
	// Make some fields bold based on status
	if (frm.doc.estado === 'Confirmada' || frm.doc.estado === 'En Proceso') {
		frm.fields_dict.valor_total.$wrapper.addClass('font-weight-bold');
	}
}

function add_status_indicator(frm) {
	let color_map = {
		'Borrador': 'gray',
		'Pendiente': 'orange',
		'Confirmada': 'blue',
		'En Proceso': 'purple',
		'Completada': 'green',
		'Cancelada': 'red'
	};
	
	frm.page.set_indicator(frm.doc.estado, color_map[frm.doc.estado]);
}

function get_email_template(frm) {
	return `
		<h3>Confirmación de Reserva</h3>
		<p><strong>Reserva:</strong> ${frm.doc.name}</p>
		<p><strong>Destino:</strong> ${frm.doc.destino}</p>
		<p><strong>Fechas:</strong> ${frm.doc.fecha_inicio} - ${frm.doc.fecha_fin}</p>
		<p><strong>Personas:</strong> ${frm.doc.num_personas_total}</p>
		<p><strong>Hotel:</strong> ${frm.doc.hotel_reservado || 'Por confirmar'}</p>
		<p><strong>Valor Total:</strong> €${frm.doc.valor_total}</p>
		<p>Gracias por su confianza.</p>
	`;
}
