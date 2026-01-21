# Copyright (c) 2024, SBC Internationals and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	chart = get_chart_data(data)
	
	return columns, data, None, chart

def get_columns():
	return [
		{
			"fieldname": "cliente",
			"label": _("Cliente"),
			"fieldtype": "Link",
			"options": "Cliente Turistico",
			"width": 200
		},
		{
			"fieldname": "tipo_cliente",
			"label": _("Tipo"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "categoria",
			"label": _("Categoría"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "total_reservas",
			"label": _("Total Reservas"),
			"fieldtype": "Int",
			"width": 120
		},
		{
			"fieldname": "reservas_completadas",
			"label": _("Completadas"),
			"fieldtype": "Int",
			"width": 120
		},
		{
			"fieldname": "reservas_canceladas",
			"label": _("Canceladas"),
			"fieldtype": "Int",
			"width": 120
		},
		{
			"fieldname": "valor_total",
			"label": _("Valor Total (€)"),
			"fieldtype": "Currency",
			"options": "EUR",
			"width": 150
		},
		{
			"fieldname": "comision_total",
			"label": _("Comisión Total (€)"),
			"fieldtype": "Currency",
			"options": "EUR",
			"width": 150
		},
		{
			"fieldname": "promedio_reserva",
			"label": _("Promedio/Reserva (€)"),
			"fieldtype": "Currency",
			"options": "EUR",
			"width": 150
		},
		{
			"fieldname": "tasa_conversion",
			"label": _("Tasa Conversión %"),
			"fieldtype": "Percent",
			"width": 130
		}
	]

def get_data(filters):
	conditions = get_conditions(filters)
	
	query = f"""
		SELECT
			c.name as cliente,
			c.tipo_cliente,
			c.categoria,
			COUNT(r.name) as total_reservas,
			SUM(CASE WHEN r.estado = 'Completada' THEN 1 ELSE 0 END) as reservas_completadas,
			SUM(CASE WHEN r.estado = 'Cancelada' THEN 1 ELSE 0 END) as reservas_canceladas,
			SUM(r.valor_total) as valor_total,
			SUM(r.comision_sbc) as comision_total,
			AVG(r.valor_total) as promedio_reserva,
			(SUM(CASE WHEN r.estado = 'Completada' THEN 1 ELSE 0 END) * 100.0 / COUNT(r.name)) as tasa_conversion
		FROM
			`tabCliente Turistico` c
		LEFT JOIN
			`tabReserva Paquete` r ON r.cliente = c.name AND r.docstatus = 1
		WHERE
			1=1 {conditions}
		GROUP BY
			c.name
		ORDER BY
			valor_total DESC
	"""
	
	return frappe.db.sql(query, filters, as_dict=1)

def get_conditions(filters):
	conditions = ""
	
	if filters.get("from_date"):
		conditions += " AND r.fecha_reserva >= %(from_date)s"
	
	if filters.get("to_date"):
		conditions += " AND r.fecha_reserva <= %(to_date)s"
	
	if filters.get("categoria"):
		conditions += " AND c.categoria = %(categoria)s"
	
	if filters.get("tipo_cliente"):
		conditions += " AND c.tipo_cliente = %(tipo_cliente)s"
	
	if filters.get("empleado_asignado"):
		conditions += " AND c.empleado_asignado = %(empleado_asignado)s"
	
	if filters.get("pais"):
		conditions += " AND c.pais = %(pais)s"
	
	return conditions

def get_chart_data(data):
	if not data:
		return None
	
	# Get top 10 clients by value
	top_clients = sorted(data, key=lambda x: x.get('valor_total') or 0, reverse=True)[:10]
	
	return {
		"data": {
			"labels": [d.get('cliente') for d in top_clients],
			"datasets": [
				{
					"name": "Valor Total",
					"values": [d.get('valor_total') or 0 for d in top_clients]
				}
			]
		},
		"type": "bar",
		"height": 300,
		"colors": ["#7cd6fd"]
	}
