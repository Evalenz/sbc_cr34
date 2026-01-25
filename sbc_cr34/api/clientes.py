"""Utilidades para importación de clientes desde CSV"""

import frappe
import csv
from io import StringIO
from frappe.utils.data import today


@frappe.whitelist()
def import_clientes_csv(csv_content):
	"""
	Importa clientes desde un archivo CSV
	Formato esperado:
	nombre_empresa, tipo_cliente, contacto_principal, email, telefono, ciudad, pais, categoria
	"""
	try:
		# Parsear el contenido CSV
		csv_file = StringIO(csv_content)
		reader = csv.DictReader(csv_file)
		
		imported_count = 0
		errors = []
		
		for row_num, row in enumerate(reader, start=2):  # start=2 porque la fila 1 es el header
			try:
				# Validar campos requeridos
				nombre_empresa = row.get('nombre_empresa', '').strip()
				tipo_cliente = row.get('tipo_cliente', '').strip()
				
				if not nombre_empresa:
					errors.append(f"Fila {row_num}: nombre_empresa es requerido")
					continue
				
				if not tipo_cliente:
					errors.append(f"Fila {row_num}: tipo_cliente es requerido")
					continue
				
				# Verificar si el cliente ya existe
				existing = frappe.db.exists('Cliente Turistico', nombre_empresa)
				if existing:
					errors.append(f"Fila {row_num}: Cliente '{nombre_empresa}' ya existe")
					continue
				
				# Crear nuevo cliente
				cliente = frappe.new_doc('Cliente Turistico')
				cliente.nombre_empresa = nombre_empresa
				cliente.tipo_cliente = tipo_cliente
				cliente.contacto_principal = row.get('contacto_principal', '').strip()
				cliente.email = row.get('email', '').strip()
				cliente.telefono = row.get('telefono', '').strip()
				cliente.telefono_movil = row.get('telefono_movil', '').strip()
				cliente.ciudad = row.get('ciudad', '').strip()
				cliente.pais = row.get('pais', '').strip()
				cliente.provincia = row.get('provincia', '').strip()
				cliente.direccion = row.get('direccion', '').strip()
				cliente.codigo_postal = row.get('codigo_postal', '').strip()
				cliente.categoria = row.get('categoria', 'Potencial').strip()
				cliente.notas = row.get('notas', '').strip()
				cliente.fecha_alta = today()
				
				# Guardar el cliente
				cliente.insert(ignore_permissions=True)
				imported_count += 1
				
			except Exception as e:
				errors.append(f"Fila {row_num}: {str(e)}")
		
		return {
			'success': True,
			'imported': imported_count,
			'errors': errors,
			'message': f'Se importaron {imported_count} clientes correctamente'
		}
		
	except Exception as e:
		return {
			'success': False,
			'message': f'Error al procesar el CSV: {str(e)}'
		}


@frappe.whitelist()
def export_clientes_csv():
	"""
	Exporta todos los clientes a formato CSV
	"""
	try:
		clientes = frappe.get_all('Cliente Turistico', 
			fields=['nombre_empresa', 'tipo_cliente', 'contacto_principal', 'email', 
					'telefono', 'ciudad', 'pais', 'categoria', 'notas'])
		
		if not clientes:
			return {
				'success': False,
				'message': 'No hay clientes para exportar'
			}
		
		# Crear contenido CSV
		csv_content = StringIO()
		fieldnames = ['nombre_empresa', 'tipo_cliente', 'contacto_principal', 'email', 
					  'telefono', 'ciudad', 'pais', 'categoria', 'notas']
		writer = csv.DictWriter(csv_content, fieldnames=fieldnames)
		writer.writeheader()
		
		for cliente in clientes:
			writer.writerow({k: cliente.get(k, '') for k in fieldnames})
		
		return {
			'success': True,
			'csv_content': csv_content.getvalue(),
			'message': f'Exportadas {len(clientes)} clientes'
		}
		
	except Exception as e:
		return {
			'success': False,
			'message': f'Error al exportar: {str(e)}'
		}


def get_cliente_stats():
	"""
	Obtiene estadísticas de clientes
	"""
	stats = {
		'total': frappe.db.count('Cliente Turistico'),
		'por_categoria': frappe.db.get_list(
			'Cliente Turistico',
			fields=['categoria', 'count(name) as cantidad'],
			group_by='categoria'
		),
		'por_tipo': frappe.db.get_list(
			'Cliente Turistico',
			fields=['tipo_cliente', 'count(name) as cantidad'],
			group_by='tipo_cliente'
		)
	}
	return stats
