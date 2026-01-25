frappe.pages['clientes_import'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Gestión de Clientes',
		single_column: false
	});
	
	// Agregar botones en la barra de herramientas
	page.add_action_item('Importar CSV', function() {
		sbc_crm.clientes.show_import_dialog();
	}, 'btn-primary');
	
	page.add_action_item('Exportar CSV', function() {
		sbc_crm.clientes.export_csv();
	});
	
	page.add_action_item('Ver Clientes', function() {
		frappe.set_route('List', 'Cliente Turistico');
	});
	
	// Contenido principal
	let content = `
		<div class="container" style="padding: 20px;">
			<div class="row">
				<div class="col-md-8">
					<div class="card">
						<div class="card-header">
							<h5>Importar Clientes desde CSV</h5>
						</div>
						<div class="card-body">
							<p>Carga un archivo CSV con información de clientes para importarlos automáticamente.</p>
							
							<h6 style="margin-top: 20px; margin-bottom: 10px;">Formato esperado del CSV:</h6>
							<pre style="background: #f5f5f5; padding: 10px; border-radius: 5px; overflow-x: auto;">nombre_empresa,tipo_cliente,contacto_principal,email,telefono,ciudad,pais,categoria
Hotel Paradise,Hotel,Juan Pérez,juan@hotel.com,+34 901 234567,Barcelona,España,Premium
Agencia Viajes XYZ,Agencia de Viajes,María García,maria@agencia.com,+34 902 345678,Madrid,España,Estándar</pre>
							
							<h6 style="margin-top: 20px; margin-bottom: 10px;">Campos:</h6>
							<ul>
								<li><strong>nombre_empresa</strong> (requerido): Nombre del cliente/empresa</li>
								<li><strong>tipo_cliente</strong> (requerido): Hotel, Cadena Hotelera, Agencia de Viajes, Touroperador, Otro</li>
								<li><strong>contacto_principal</strong>: Nombre del contacto principal</li>
								<li><strong>email</strong>: Correo electrónico</li>
								<li><strong>telefono</strong>: Número de teléfono</li>
								<li><strong>telefono_movil</strong>: Móvil (opcional)</li>
								<li><strong>ciudad</strong>: Ciudad</li>
								<li><strong>provincia</strong>: Provincia (opcional)</li>
								<li><strong>pais</strong>: País</li>
								<li><strong>codigo_postal</strong>: Código postal (opcional)</li>
								<li><strong>direccion</strong>: Dirección (opcional)</li>
								<li><strong>categoria</strong>: Premium, Estándar, Potencial, Inactivo</li>
								<li><strong>notas</strong>: Notas adicionales (opcional)</li>
							</ul>
							
							<button class="btn btn-primary" onclick="sbc_crm.clientes.show_import_dialog()">
								<span class="octicon octicon-upload"></span> Seleccionar archivo CSV
							</button>
						</div>
					</div>
				</div>
				
				<div class="col-md-4">
					<div class="card">
						<div class="card-header">
							<h5>Acciones Rápidas</h5>
						</div>
						<div class="card-body">
							<div class="list-group">
								<a href="javascript:void(0)" class="list-group-item list-group-item-action" 
									onclick="frappe.set_route('List', 'Cliente Turistico')">
									<div style="font-weight: 500;">Ver todos los clientes</div>
									<small>Gestiona la lista completa de clientes</small>
								</a>
								<a href="javascript:void(0)" class="list-group-item list-group-item-action" 
									onclick="sbc_crm.clientes.export_csv()">
									<div style="font-weight: 500;">Descargar plantilla CSV</div>
									<small>Exporta los clientes actuales</small>
								</a>
								<a href="javascript:void(0)" class="list-group-item list-group-item-action" 
									onclick="frappe.new_doc('Cliente Turistico')">
									<div style="font-weight: 500;">Crear nuevo cliente</div>
									<small>Añade un cliente manualmente</small>
								</a>
							</div>
							
							<div class="card" style="margin-top: 20px;">
								<div class="card-header">
									<h6>Estadísticas</h6>
								</div>
								<div class="card-body" id="stats-container">
									<div style="text-align: center; padding: 20px;">
										<i class="fa fa-spinner fa-spin"></i> Cargando...
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	`;
	
	page.main.html(content);
	
	// Cargar estadísticas
	frappe.call({
		method: 'sbc_cr34.api.clientes.get_cliente_stats',
		callback: function(r) {
			if (r.message) {
				let stats = r.message;
				let html = `<p><strong>Total de clientes:</strong> ${stats.total}</p>`;
				
				if (stats.por_categoria && stats.por_categoria.length > 0) {
					html += '<p><strong>Por categoría:</strong></p><ul>';
					stats.por_categoria.forEach(item => {
						html += `<li>${item.categoria}: ${item.cantidad}</li>`;
					});
					html += '</ul>';
				}
				
				if (stats.por_tipo && stats.por_tipo.length > 0) {
					html += '<p><strong>Por tipo:</strong></p><ul>';
					stats.por_tipo.forEach(item => {
						html += `<li>${item.tipo_cliente}: ${item.cantidad}</li>`;
					});
					html += '</ul>';
				}
				
				$('#stats-container').html(html);
			}
		}
	});
};
