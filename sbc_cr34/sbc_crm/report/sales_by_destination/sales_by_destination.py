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
			"fieldname": "destino",
			"label": _("Destino"),
			"fieldtype": "Data",
			"width": 180
		},
		{
			"fieldname": "pais_destino",
			"label": _("País"),
			"fieldtype": "Link",
			"options": "Country",
			"width": 150
		},
		{
			"fieldname": "total_reservas",
			"label": _("Reservas"),
			"fieldtype": "Int",
			"width": 100
		},
		{
			"fieldname": "total_personas",
			"label": _("Total Personas"),
			"fieldtype": "Int",
			"width": 120
		},
		{
			"fieldname": "total_noches",
			"label": _("Total Noches"),
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
			"label": _("Comisión (€)"),
			"fieldtype": "Currency",
			"options": "EUR",
			"width": 150
		},
		{
			"fieldname": "promedio_persona",
			"label": _("Promedio/Persona (€)"),
			"fieldtype": "Currency",
			"options": "EUR",
			"width": 160
		}
	]

def get_data(filters):
	conditions = get_conditions(filters)
	
	query = f"""
		SELECT
			destino,
			pais_destino,
			COUNT(*) as total_reservas,
			SUM(num_personas_total) as total_personas,
			SUM(num_noches) as total_noches,
			SUM(valor_total) as valor_total,
			SUM(comision_sbc) as comision_total,
			AVG(valor_total / NULLIF(num_personas_total, 0)) as promedio_persona
		FROM
			`tabReserva Paquete`
		WHERE
			docstatus = 1
			AND estado != 'Cancelada'
			{conditions}
		GROUP BY
			destino, pais_destino
		ORDER BY
			valor_total DESC
	"""
	
	return frappe.db.sql(query, filters, as_dict=1)

def get_conditions(filters):
	conditions = ""
	
	if filters.get("from_date"):
		conditions += " AND fecha_inicio >= %(from_date)s"
	
	if filters.get("to_date"):
		conditions += " AND fecha_inicio <= %(to_date)s"
	
	if filters.get("pais_destino"):
		conditions += " AND pais_destino = %(pais_destino)s"
	
	if filters.get("cliente"):
		conditions += " AND cliente = %(cliente)s"
	
	if filters.get("estado"):
		conditions += " AND estado = %(estado)s"
	
	return conditions

def get_chart_data(data):
	if not data:
		return None
	
	# Get top 10 destinations
	top_destinations = data[:10]
	
	return {
		"data": {
			"labels": [d.get('destino') for d in top_destinations],
			"datasets": [
				{
					"name": "Reservas",
					"values": [d.get('total_reservas') for d in top_destinations]
				},
				{
					"name": "Valor Total (€/1000)",
					"values": [round((d.get('valor_total') or 0) / 1000, 2) for d in top_destinations]
				}
			]
		},
		"type": "bar",
		"height": 300,
		"colors": ["#7cd6fd", "#5e64ff"]
	}
