# -*- coding: utf-8 -*-
# Copyright (c) 2024, SBC Internationals and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import add_to_date, get_datetime

class ActividadComercial(Document):
	def validate(self):
		"""Validate document before saving"""
		self.calculate_end_time()
		self.validate_datetime()
	
	def on_update(self):
		"""Actions after document update"""
		if self.crear_seguimiento and self.fecha_seguimiento and self.estado == "Completada":
			self.create_followup_activity()
	
	def calculate_end_time(self):
		"""Calculate end time based on start time and duration"""
		if self.fecha_hora and self.duracion_minutos:
			start_datetime = get_datetime(self.fecha_hora)
			self.fecha_fin = add_to_date(start_datetime, minutes=self.duracion_minutos)
	
	def validate_datetime(self):
		"""Validate datetime logic"""
		if self.fecha_hora and self.fecha_fin:
			if get_datetime(self.fecha_fin) < get_datetime(self.fecha_hora):
				frappe.throw("La fecha fin no puede ser anterior a la fecha de inicio")
	
	def create_followup_activity(self):
		"""Create a follow-up activity"""
		# Check if followup already created
		if frappe.db.exists("Actividad Comercial", {
			"titulo": f"Seguimiento: {self.titulo}",
			"fecha_hora": [">=", self.fecha_hora]
		}):
			return
		
		followup = frappe.get_doc({
			"doctype": "Actividad Comercial",
			"titulo": f"Seguimiento: {self.titulo}",
			"tipo_actividad": "Seguimiento",
			"estado": "Programada",
			"prioridad": self.prioridad,
			"cliente": self.cliente,
			"reserva_relacionada": self.reserva_relacionada,
			"empleado_responsable": self.empleado_responsable,
			"fecha_hora": f"{self.fecha_seguimiento} 09:00:00",
			"duracion_minutos": 30,
			"descripcion": f"<p>Seguimiento de actividad: {self.name}</p><p>Próximos pasos: {self.proximos_pasos or ''}</p>"
		})
		
		try:
			followup.insert(ignore_permissions=False)
			frappe.msgprint(f"Actividad de seguimiento creada: {followup.name}", 
				indicator='green', alert=True)
			# Uncheck to avoid recreating
			self.db_set('crear_seguimiento', 0, update_modified=False)
		except Exception as e:
			frappe.log_error(f"Error creating followup activity: {str(e)}")


@frappe.whitelist()
def get_upcoming_activities(employee=None, days=7):
	"""Get upcoming activities for an employee"""
	from frappe.utils import today, add_days
	
	filters = {
		"fecha_hora": ["between", [today(), add_days(today(), days)]],
		"estado": ["in", ["Programada", "En Curso"]]
	}
	
	if employee:
		filters["empleado_responsable"] = employee
	
	activities = frappe.get_all(
		"Actividad Comercial",
		filters=filters,
		fields=["name", "titulo", "tipo_actividad", "fecha_hora", "cliente", 
				"estado", "prioridad", "ubicacion"],
		order_by="fecha_hora asc"
	)
	
	return activities


@frappe.whitelist()
def mark_as_completed(activity_name):
	"""Quick action to mark activity as completed"""
	doc = frappe.get_doc("Actividad Comercial", activity_name)
	doc.estado = "Completada"
	doc.save()
	frappe.db.commit()
	
	return {"success": True, "message": f"Actividad {activity_name} marcada como completada"}
