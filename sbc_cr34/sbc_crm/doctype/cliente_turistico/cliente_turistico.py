# -*- coding: utf-8 -*-
# Copyright (c) 2024, SBC Internationals and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import validate_email_address

class ClienteTuristico(Document):
	def validate(self):
		"""Validate document before saving"""
		self.validate_email()
		self.validate_additional_contacts()
		self.update_category_based_on_volume()
	
	def validate_email(self):
		"""Validate main email address"""
		if self.email:
			try:
				validate_email_address(self.email, throw=True)
			except Exception as e:
				frappe.throw(f"Email principal inválido: {str(e)}")
	
	def validate_additional_contacts(self):
		"""Validate emails in additional contacts table"""
		if self.contactos_adicionales:
			for contact in self.contactos_adicionales:
				if contact.email:
					try:
						validate_email_address(contact.email, throw=True)
					except Exception as e:
						frappe.throw(f"Email inválido en contacto adicional '{contact.nombre}': {str(e)}")
	
	def update_category_based_on_volume(self):
		"""Auto-update category based on annual volume"""
		if self.volumen_anual_estimado:
			if self.volumen_anual_estimado >= 100000:
				suggested_category = "Premium"
			elif self.volumen_anual_estimado >= 50000:
				suggested_category = "Estándar"
			else:
				suggested_category = "Potencial"
			
			# Only suggest if current category is "Potencial"
			if self.categoria == "Potencial" and suggested_category != "Potencial":
				frappe.msgprint(
					f"Sugerencia: El volumen anual sugiere categoría '{suggested_category}'",
					indicator='blue',
					alert=True
				)


@frappe.whitelist()
def get_client_summary(client_name):
	"""Get comprehensive summary of client activity"""
	if not frappe.db.exists("Cliente Turistico", client_name):
		return None
	
	# Get basic client info
	client = frappe.get_doc("Cliente Turistico", client_name)
	
	# Get reservation statistics
	reservations = frappe.db.sql("""
		SELECT 
			COUNT(*) as total_reservas,
			SUM(CASE WHEN estado = 'Completada' THEN 1 ELSE 0 END) as completadas,
			SUM(CASE WHEN estado = 'Cancelada' THEN 1 ELSE 0 END) as canceladas,
			SUM(valor_total) as valor_total,
			SUM(comision_sbc) as comision_total
		FROM `tabReserva Paquete`
		WHERE cliente = %s AND docstatus = 1
	""", client_name, as_dict=True)[0]
	
	# Get recent activities
	activities = frappe.get_all(
		"Actividad Comercial",
		filters={"cliente": client_name},
		fields=["name", "titulo", "tipo_actividad", "fecha_hora", "estado"],
		order_by="fecha_hora desc",
		limit=5
	)
	
	# Get upcoming reservations
	upcoming = frappe.get_all(
		"Reserva Paquete",
		filters={
			"cliente": client_name,
			"fecha_inicio": [">=", frappe.utils.today()],
			"estado": ["in", ["Confirmada", "En Proceso"]]
		},
		fields=["name", "titulo_reserva", "fecha_inicio", "destino", "valor_total"],
		order_by="fecha_inicio asc",
		limit=5
	)
	
	return {
		"client": client,
		"reservations_stats": reservations,
		"recent_activities": activities,
		"upcoming_reservations": upcoming
	}


@frappe.whitelist()
def mark_as_inactive(client_name):
	"""Mark client as inactive"""
	doc = frappe.get_doc("Cliente Turistico", client_name)
	doc.categoria = "Inactivo"
	doc.save()
	
	return {"success": True, "message": f"Cliente {client_name} marcado como Inactivo"}


@frappe.whitelist()
def export_client_contacts(client_name):
	"""Export all contacts for a client"""
	client = frappe.get_doc("Cliente Turistico", client_name)
	
	contacts = [{
		"nombre": client.contacto_principal,
		"cargo": client.cargo,
		"email": client.email,
		"telefono": client.telefono,
		"tipo": "Principal"
	}]
	
	if client.contactos_adicionales:
		for contact in client.contactos_adicionales:
			contacts.append({
				"nombre": contact.nombre,
				"cargo": contact.cargo,
				"email": contact.email,
				"telefono": contact.telefono,
				"tipo": "Adicional"
			})
	
	return contacts
