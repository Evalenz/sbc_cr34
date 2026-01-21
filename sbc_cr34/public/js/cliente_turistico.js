// Client Script for Cliente Turistico
// Copyright (c) 2024, SBC Internationals

frappe.ui.form.on('Cliente Turistico', {
	refresh: function(frm) {
		// Add custom buttons
		if (!frm.is_new()) {
			add_custom_buttons(frm);
			load_client_dashboard(frm);
		}
		
		// Set field dependencies
		set_field_dependencies(frm);
		
		// Add category indicator
		add_category_indicator(frm);
	},
	
	tipo_cliente: function(frm) {
		// Show/hide stars field based on client type
		set_field_dependencies(frm);
	},
	
	email: function(frm) {
		// Validate email format
		if (frm.doc.email) {
			validate_email_field(frm, 'email');
		}
	},
	
	volumen_anual_estimado: function(frm) {
		// Suggest category based on volume
		suggest_category(frm);
	},
	
	categoria: function(frm) {
		add_category_indicator(frm);
	}
});

// Child table: Cliente Contacto Adicional
frappe.ui.form.on('Cliente Contacto Adicional', {
	email: function(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		if (row.email) {
			// Basic email validation
			if (!row.email.includes('@')) {
				frappe.msgprint(__('Email inválido'));
			}
		}
	}
});

// Helper Functions

function add_custom_buttons(frm) {
	// View all reservations
	frm.add_custom_button(__('Ver Reservas'), function() {
		frappe.set_route('List', 'Reserva Paquete', {
			'cliente': frm.doc.name
		});
	}, __('Ver'));
	
	// View all activities
	frm.add_custom_button(__('Ver Actividades'), function() {
		frappe.set_route('List', 'Actividad Comercial', {
			'cliente': frm.doc.name
		});
	}, __('Ver'));
	
	// Create new reservation
	frm.add_custom_button(__('Nueva Reserva'), function() {
		frappe.new_doc('Reserva Paquete', {
			cliente: frm.doc.name,
			empleado_responsable: frm.doc.empleado_asignado,
			porcentaje_comision: frm.doc.comision_estandar
		});
	}, __('Crear'));
	
	// Create new activity
	frm.add_custom_button(__('Nueva Actividad'), function() {
		frappe.new_doc('Actividad Comercial', {
			cliente: frm.doc.name,
			empleado_responsable: frm.doc.empleado_asignado || frappe.session.user
		});
	}, __('Crear'));
	
	// Export contacts
	frm.add_custom_button(__('Exportar Contactos'), function() {
		frappe.call({
			method: 'sbc_cr34.sbc_crm.doctype.cliente_turistico.cliente_turistico.export_client_contacts',
			args: {
				client_name: frm.doc.name
			},
			callback: function(r) {
				if (r.message) {
					download_contacts_csv(r.message, frm.doc.nombre_empresa);
				}
			}
		});
	}, __('Acciones'));
	
	// Mark as inactive
	if (frm.doc.categoria !== 'Inactivo') {
		frm.add_custom_button(__('Marcar como Inactivo'), function() {
			frappe.confirm(
				'¿Está seguro de marcar este cliente como Inactivo?',
				() => {
					frappe.call({
						method: 'sbc_cr34.sbc_crm.doctype.cliente_turistico.cliente_turistico.mark_as_inactive',
						args: {
							client_name: frm.doc.name
						},
						callback: function(r) {
							frm.reload_doc();
						}
					});
				}
			);
		}, __('Acciones'));
	}
}

function set_field_dependencies(frm) {
	// Show stars field only for hotels
	let show_stars = frm.doc.tipo_cliente === 'Hotel' || frm.doc.tipo_cliente === 'Cadena Hotelera';
	frm.toggle_display('estrellas', show_stars);
	
	if (show_stars) {
		frm.set_df_property('estrellas', 'reqd', 1);
	} else {
		frm.set_df_property('estrellas', 'reqd', 0);
	}
}

function validate_email_field(frm, fieldname) {
	let email = frm.doc[fieldname];
	let email_regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
	
	if (!email_regex.test(email)) {
		frappe.msgprint({
			title: __('Email Inválido'),
			indicator: 'red',
			message: __('Por favor ingrese un email válido')
		});
	}
}

function suggest_category(frm) {
	if (!frm.doc.volumen_anual_estimado) return;
	
	let suggested = '';
	let volume = frm.doc.volumen_anual_estimado;
	
	if (volume >= 100000) {
		suggested = 'Premium';
	} else if (volume >= 50000) {
		suggested = 'Estándar';
	} else {
		suggested = 'Potencial';
	}
	
	if (frm.doc.categoria === 'Potencial' && suggested !== 'Potencial') {
		frappe.msgprint({
			title: __('Sugerencia de Categoría'),
			indicator: 'blue',
			message: __(`Basado en el volumen anual (€${volume}), se sugiere categoría: <strong>${suggested}</strong>`)
		});
	}
}

function add_category_indicator(frm) {
	let color_map = {
		'Premium': 'green',
		'Estándar': 'blue',
		'Potencial': 'orange',
		'Inactivo': 'red'
	};
	
	if (frm.doc.categoria) {
		frm.page.set_indicator(frm.doc.categoria, color_map[frm.doc.categoria]);
	}
}

function load_client_dashboard(frm) {
	// Load client summary in a custom section
	frappe.call({
		method: 'sbc_cr34.sbc_crm.doctype.cliente_turistico.cliente_turistico.get_client_summary',
		args: {
			client_name: frm.doc.name
		},
		callback: function(r) {
			if (r.message) {
				render_dashboard(frm, r.message);
			}
		}
	});
}

function render_dashboard(frm, data) {
	// Create dashboard HTML
	let stats = data.reservations_stats;
	
	let html = `
		<div class="row">
			<div class="col-md-3">
				<div class="card text-center">
					<div class="card-body">
						<h5 class="card-title">${stats.total_reservas || 0}</h5>
						<p class="card-text text-muted">Total Reservas</p>
					</div>
				</div>
			</div>
			<div class="col-md-3">
				<div class="card text-center">
					<div class="card-body">
						<h5 class="card-title">${stats.completadas || 0}</h5>
						<p class="card-text text-muted">Completadas</p>
					</div>
				</div>
			</div>
			<div class="col-md-3">
				<div class="card text-center">
					<div class="card-body">
						<h5 class="card-title">€${format_currency(stats.valor_total || 0)}</h5>
						<p class="card-text text-muted">Valor Total</p>
					</div>
				</div>
			</div>
			<div class="col-md-3">
				<div class="card text-center">
					<div class="card-body">
						<h5 class="card-title">€${format_currency(stats.comision_total || 0)}</h5>
						<p class="card-text text-muted">Comisiones</p>
					</div>
				</div>
			</div>
		</div>
	`;
	
	// Add to form
	if (!frm.fields_dict.dashboard_html) {
		frm.add_custom_button(__('Actualizar Dashboard'), function() {
			load_client_dashboard(frm);
		});
	}
}

function format_currency(value) {
	return new Intl.NumberFormat('es-ES', {
		minimumFractionDigits: 2,
		maximumFractionDigits: 2
	}).format(value);
}

function download_contacts_csv(contacts, client_name) {
	// Convert contacts to CSV
	let csv = 'Nombre,Cargo,Email,Telefono,Tipo\n';
	contacts.forEach(function(contact) {
		csv += `"${contact.nombre}","${contact.cargo || ''}","${contact.email || ''}","${contact.telefono || ''}","${contact.tipo}"\n`;
	});
	
	// Trigger download
	let blob = new Blob([csv], { type: 'text/csv' });
	let url = window.URL.createObjectURL(blob);
	let a = document.createElement('a');
	a.href = url;
	a.download = `contactos_${client_name.replace(/ /g, '_')}.csv`;
	document.body.appendChild(a);
	a.click();
	document.body.removeChild(a);
	window.URL.revokeObjectURL(url);
}
