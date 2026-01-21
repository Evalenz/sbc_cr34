# -*- coding: utf-8 -*-
# Copyright (c) 2024, SBC Internationals and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import today, add_days, now_datetime
from frappe import _

def send_daily_activity_reminder():
	"""Send daily reminders for upcoming activities"""
	
	# Get activities for today and tomorrow
	activities = frappe.get_all(
		"Actividad Comercial",
		filters={
			"fecha_hora": ["between", [today(), add_days(today(), 1)]],
			"estado": ["in", ["Programada", "En Curso"]]
		},
		fields=["name", "titulo", "tipo_actividad", "fecha_hora", 
				"empleado_responsable", "cliente", "ubicacion"]
	)
	
	if not activities:
		return
	
	# Group by employee
	employee_activities = {}
	for activity in activities:
		emp = activity.empleado_responsable
		if emp not in employee_activities:
			employee_activities[emp] = []
		employee_activities[emp].append(activity)
	
	# Send emails
	for employee, acts in employee_activities.items():
		send_activity_reminder_email(employee, acts)
	
	frappe.db.commit()


def send_activity_reminder_email(employee, activities):
	"""Send email reminder to employee"""
	
	subject = f"Recordatorio: {len(activities)} actividad(es) próxima(s)"
	
	message = f"""
	<h3>Actividades Programadas</h3>
	<p>Tiene {len(activities)} actividad(es) programada(s) para hoy/mañana:</p>
	<table border="1" cellpadding="5" style="border-collapse: collapse;">
		<tr>
			<th>Actividad</th>
			<th>Tipo</th>
			<th>Fecha/Hora</th>
			<th>Cliente</th>
			<th>Ubicación</th>
		</tr>
	"""
	
	for act in activities:
		message += f"""
		<tr>
			<td>{act.titulo}</td>
			<td>{act.tipo_actividad}</td>
			<td>{act.fecha_hora}</td>
			<td>{act.cliente or '-'}</td>
			<td>{act.ubicacion or '-'}</td>
		</tr>
		"""
	
	message += """
	</table>
	<br>
	<p>Acceda al sistema para ver más detalles.</p>
	"""
	
	frappe.sendmail(
		recipients=employee,
		subject=subject,
		message=message,
		delayed=False
	)


def update_client_categories():
	"""Automatically update client categories based on activity"""
	
	# Get clients with completed reservations
	clients = frappe.db.sql("""
		SELECT 
			c.name,
			c.categoria,
			COUNT(r.name) as total_reservas,
			SUM(r.valor_total) as valor_total,
			MAX(r.fecha_reserva) as ultima_reserva
		FROM 
			`tabCliente Turistico` c
		LEFT JOIN 
			`tabReserva Paquete` r ON r.cliente = c.name 
			AND r.docstatus = 1 
			AND r.estado = 'Completada'
		GROUP BY 
			c.name
	""", as_dict=True)
	
	updates_made = 0
	
	for client in clients:
		old_category = client.categoria
		new_category = determine_category(client)
		
		if old_category != new_category:
			frappe.db.set_value('Cliente Turistico', client.name, 'categoria', new_category)
			updates_made += 1
	
	if updates_made > 0:
		frappe.db.commit()
		frappe.logger().info(f"Updated {updates_made} client categories")


def determine_category(client_data):
	"""Determine client category based on performance"""
	
	valor_total = client_data.get('valor_total') or 0
	total_reservas = client_data.get('total_reservas') or 0
	ultima_reserva = client_data.get('ultima_reserva')
	
	# Check if inactive (no reservation in last 12 months)
	if ultima_reserva:
		from frappe.utils import date_diff, today
		days_since_last = date_diff(today(), ultima_reserva)
		if days_since_last > 365:
			return "Inactivo"
	
	# Categorize based on value and volume
	if valor_total >= 50000 or total_reservas >= 10:
		return "Premium"
	elif valor_total >= 20000 or total_reservas >= 5:
		return "Estándar"
	else:
		return "Potencial"


def send_weekly_sales_report():
	"""Send weekly sales report to managers"""
	
	# Get Sales Master Managers
	managers = frappe.get_all(
		"User",
		filters={
			"enabled": 1,
			"name": ["in", [
				user.parent for user in frappe.get_all(
					"Has Role",
					filters={"role": "Sales Master Manager"},
					fields=["parent"]
				)
			]]
		},
		fields=["email", "full_name"]
	)
	
	if not managers:
		return
	
	# Get weekly statistics
	from frappe.utils import add_days, today
	start_date = add_days(today(), -7)
	
	stats = frappe.db.sql("""
		SELECT
			COUNT(*) as total_reservas,
			SUM(CASE WHEN estado = 'Confirmada' THEN 1 ELSE 0 END) as confirmadas,
			SUM(CASE WHEN estado = 'Completada' THEN 1 ELSE 0 END) as completadas,
			SUM(valor_total) as valor_total,
			SUM(comision_sbc) as comision_total
		FROM
			`tabReserva Paquete`
		WHERE
			fecha_reserva >= %s
			AND docstatus = 1
	""", start_date, as_dict=True)[0]
	
	# Get top performers
	top_employees = frappe.db.sql("""
		SELECT
			empleado_responsable,
			COUNT(*) as reservas,
			SUM(valor_total) as valor
		FROM
			`tabReserva Paquete`
		WHERE
			fecha_reserva >= %s
			AND docstatus = 1
			AND empleado_responsable IS NOT NULL
		GROUP BY
			empleado_responsable
		ORDER BY
			valor DESC
		LIMIT 5
	""", start_date, as_dict=True)
	
	# Build email
	subject = "Reporte Semanal de Ventas - SBC CRM"
	
	message = f"""
	<h2>Reporte Semanal de Ventas</h2>
	<p>Período: {start_date} - {today()}</p>
	
	<h3>Resumen General</h3>
	<ul>
		<li><strong>Total Reservas:</strong> {stats.total_reservas}</li>
		<li><strong>Confirmadas:</strong> {stats.confirmadas}</li>
		<li><strong>Completadas:</strong> {stats.completadas}</li>
		<li><strong>Valor Total:</strong> €{stats.valor_total:,.2f}</li>
		<li><strong>Comisión Total:</strong> €{stats.comision_total:,.2f}</li>
	</ul>
	
	<h3>Top 5 Empleados</h3>
	<table border="1" cellpadding="5" style="border-collapse: collapse;">
		<tr>
			<th>Empleado</th>
			<th>Reservas</th>
			<th>Valor</th>
		</tr>
	"""
	
	for emp in top_employees:
		message += f"""
		<tr>
			<td>{emp.empleado_responsable}</td>
			<td>{emp.reservas}</td>
			<td>€{emp.valor:,.2f}</td>
		</tr>
		"""
	
	message += """
	</table>
	<br>
	<p>Acceda al sistema para ver informes detallados.</p>
	"""
	
	# Send to all managers
	for manager in managers:
		frappe.sendmail(
			recipients=manager.email,
			subject=subject,
			message=message,
			delayed=False
		)
	
	frappe.db.commit()


def generate_monthly_analytics():
	"""Generate monthly analytics and store for reporting"""
	
	from frappe.utils import get_first_day, get_last_day, add_months
	
	# Get last month's dates
	today_date = today()
	first_day = get_first_day(add_months(today_date, -1))
	last_day = get_last_day(add_months(today_date, -1))
	
	# Calculate metrics
	metrics = frappe.db.sql("""
		SELECT
			COUNT(*) as total_reservas,
			SUM(CASE WHEN estado = 'Completada' THEN 1 ELSE 0 END) as completadas,
			SUM(CASE WHEN estado = 'Cancelada' THEN 1 ELSE 0 END) as canceladas,
			SUM(valor_total) as valor_total,
			SUM(comision_sbc) as comision_total,
			AVG(valor_total) as promedio_reserva,
			COUNT(DISTINCT cliente) as clientes_unicos
		FROM
			`tabReserva Paquete`
		WHERE
			fecha_reserva BETWEEN %s AND %s
			AND docstatus = 1
	""", (first_day, last_day), as_dict=True)[0]
	
	# Log analytics
	frappe.logger().info(f"Monthly Analytics for {first_day} - {last_day}: {metrics}")
	
	# You could store this in a custom DocType for historical tracking
	# create_analytics_record(first_day, last_day, metrics)
	
	frappe.db.commit()
