# Copyright (c) 2024, SBC Internationals and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import today, add_days

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	summary = get_summary(data)
	chart = get_chart_data(data)
	
	return columns, data, None, chart, summary

def get_columns():
	return [
		{
			"fieldname": "name",
			"label": _("ID"),
			"fieldtype": "Link",
			"options": "Actividad Comercial",
			"width": 120
		},
		{
			"fieldname": "titulo",
			"label": _("Título"),
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "tipo_actividad",
			"label": _("Tipo"),
			"fieldtype": "Data",
			"width": 130
		},
		{
			"fieldname": "cliente",
			"label": _("Cliente"),
			"fieldtype": "Link",
			"options": "Cliente Turistico",
			"width": 180
		},
		{
			"fieldname": "fecha_hora",
			"label": _("Fecha/Hora"),
			"fieldtype": "Datetime",
			"width": 160
		},
		{
			"fieldname": "estado",
			"label": _("Estado"),
			"fieldtype": "Data",
			"width": 110
		},
		{
			"fieldname": "prioridad",
			"label": _("Prioridad"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "empleado_responsable",
			"label": _("Responsable"),
			"fieldtype": "Link",
			"options": "User",
			"width": 150
		},
		{
			"fieldname": "resultado",
			"label": _("Resultado"),
			"fieldtype": "Data",
			"width": 150
		}
	]

def get_data(filters):
	conditions = get_conditions(filters)
	
	query = f"""
		SELECT
			name,
			titulo,
			tipo_actividad,
			cliente,
			fecha_hora,
			estado,
			prioridad,
			empleado_responsable,
			resultado
		FROM
			`tabActividad Comercial`
		WHERE
			1=1 {conditions}
		ORDER BY
			fecha_hora DESC
	"""
	
	return frappe.db.sql(query, filters, as_dict=1)

def get_conditions(filters):
	conditions = ""
	
	if filters.get("from_date"):
		conditions += " AND DATE(fecha_hora) >= %(from_date)s"
	
	if filters.get("to_date"):
		conditions += " AND DATE(fecha_hora) <= %(to_date)s"
	
	if filters.get("empleado_responsable"):
		conditions += " AND empleado_responsable = %(empleado_responsable)s"
	
	if filters.get("cliente"):
		conditions += " AND cliente = %(cliente)s"
	
	if filters.get("tipo_actividad"):
		conditions += " AND tipo_actividad = %(tipo_actividad)s"
	
	if filters.get("estado"):
		conditions += " AND estado = %(estado)s"
	
	if filters.get("prioridad"):
		conditions += " AND prioridad = %(prioridad)s"
	
	# Show upcoming activities by default
	if not filters.get("show_all"):
		conditions += f" AND fecha_hora >= '{today()}'"
	
	return conditions

def get_summary(data):
	if not data:
		return []
	
	total = len(data)
	programadas = len([d for d in data if d.get('estado') == 'Programada'])
	completadas = len([d for d in data if d.get('estado') == 'Completada'])
	en_curso = len([d for d in data if d.get('estado') == 'En Curso'])
	canceladas = len([d for d in data if d.get('estado') == 'Cancelada'])
	
	return [
		{
			"value": total,
			"label": _("Total Actividades"),
			"datatype": "Int",
			"indicator": "blue"
		},
		{
			"value": programadas,
			"label": _("Programadas"),
			"datatype": "Int",
			"indicator": "orange"
		},
		{
			"value": en_curso,
			"label": _("En Curso"),
			"datatype": "Int",
			"indicator": "yellow"
		},
		{
			"value": completadas,
			"label": _("Completadas"),
			"datatype": "Int",
			"indicator": "green"
		},
		{
			"value": canceladas,
			"label": _("Canceladas"),
			"datatype": "Int",
			"indicator": "red"
		}
	]

def get_chart_data(data):
	if not data:
		return None
	
	# Group by type
	type_counts = {}
	for d in data:
		tipo = d.get('tipo_actividad')
		if tipo:
			type_counts[tipo] = type_counts.get(tipo, 0) + 1
	
	return {
		"data": {
			"labels": list(type_counts.keys()),
			"datasets": [
				{
					"name": "Actividades por Tipo",
					"values": list(type_counts.values())
				}
			]
		},
		"type": "pie",
		"height": 300
	}
