// Script para importación de clientes desde CSV
frappe.provide('sbc_crm.clientes');

sbc_crm.clientes.show_import_dialog = function() {
	const d = new frappe.ui.Dialog({
		title: 'Importar Clientes desde CSV',
		fields: [
			{
				label: 'Archivo CSV',
				fieldname: 'csv_file',
				fieldtype: 'Attach',
				reqd: 1,
				description: 'Columnas esperadas: nombre_empresa, tipo_cliente, contacto_principal, email, telefono, ciudad, pais, categoria'
			}
		],
		primary_action_label: 'Importar',
		primary_action(values) {
			if (!values.csv_file) {
				frappe.msgprint('Por favor selecciona un archivo CSV');
				return;
			}
			
			frappe.call({
				method: 'frappe.client.get_value',
				args: {
					doctype: 'File',
					filters: { file_url: values.csv_file }
				},
				callback: function(r) {
					if (r.message) {
						fetch(r.message.file_url)
							.then(response => response.text())
							.then(csv_content => {
								sbc_crm.clientes.import_clientes(csv_content, d);
							})
							.catch(error => {
								frappe.msgprint(`Error: ${error}`);
							});
					}
				}
			});
		}
	});
	d.show();
};

sbc_crm.clientes.import_clientes = function(csv_content, dialog) {
	frappe.call({
		method: 'sbc_cr34.api.clientes.import_clientes_csv',
		args: { csv_content: csv_content },
		callback: function(r) {
			dialog.hide();
			if (r.message) {
				let html = `<div style="padding: 10px;">
					<p><strong>${r.message.message}</strong></p>`;
				
				if (r.message.imported > 0) {
					html += `<p style="color: green;">✓ Importados: ${r.message.imported} clientes</p>`;
				}
				
				if (r.message.errors.length > 0) {
					html += `<div style="background: #fff3cd; padding: 10px; margin-top: 10px; border-radius: 5px;">
						<strong>Errores:</strong>
						<ul style="margin: 10px 0;">`;
					r.message.errors.forEach(e => {
						html += `<li>${e}</li>`;
					});
					html += `</ul></div>`;
				}
				html += `</div>`;
				
				frappe.msgprint({ 
					message: html, 
					title: 'Importación de Clientes'
				});
				
				if (cur_list) cur_list.refresh();
			}
		}
	});
};

sbc_crm.clientes.export_csv = function() {
	frappe.call({
		method: 'sbc_cr34.api.clientes.export_clientes_csv',
		callback: function(r) {
			if (r.message.success) {
				const element = document.createElement('a');
				element.setAttribute('href', 'data:text/csv;charset=utf-8,' + 
					encodeURIComponent(r.message.csv_content));
				element.setAttribute('download', `clientes_${frappe.datetime.now_date()}.csv`);
				element.style.display = 'none';
				document.body.appendChild(element);
				element.click();
				document.body.removeChild(element);
				
				frappe.msgprint(r.message.message);
			}
		}
	});
};
