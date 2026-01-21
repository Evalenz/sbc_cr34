# -*- coding: utf-8 -*-
# Copyright (c) 2024, SBC Internationals and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import getdate, date_diff, now_datetime, add_to_date

class ReservaPaquete(Document):
	def validate(self):
		"""Validate document before saving"""
		self.calculate_nights()
		self.calculate_total_persons()
		self.calculate_additional_services_total()
		self.calculate_discount()
		self.calculate_total()
		self.calculate_commission()
		self.validate_dates()
		self.set_commission_from_client()
	
	def on_submit(self):
		"""Actions when document is submitted"""
		if self.estado == "Borrador":
			self.db_set('estado', 'Confirmada')
		self.db_set('fecha_confirmacion', now_datetime())
	
	def on_update_after_submit(self):
		"""Handle status changes after submission"""
		if self.estado == "Completada" and not self.fecha_completada:
			self.db_set('fecha_completada', now_datetime())
	
	def calculate_nights(self):
		"""Calculate number of nights between start and end dates"""
		if self.fecha_inicio and self.fecha_fin:
			start = getdate(self.fecha_inicio)
			end = getdate(self.fecha_fin)
			nights = date_diff(end, start)
			if nights < 0:
				frappe.throw("La fecha de fin debe ser posterior a la fecha de inicio")
			self.num_noches = nights
	
	def calculate_total_persons(self):
		"""Calculate total number of persons"""
		self.num_personas_total = (
			(self.num_adultos or 0) + 
			(self.num_ninos or 0) + 
			(self.num_bebes or 0)
		)
	
	def calculate_additional_services_total(self):
		"""Calculate total from additional services table"""
		total = 0
		if self.servicios_adicionales:
			for service in self.servicios_adicionales:
				# Calculate each service line total
				service.total = (service.cantidad or 0) * (service.precio_unitario or 0)
				total += service.total
		self.valor_servicios_adicionales = total
	
	def calculate_discount(self):
		"""Calculate discount amount from percentage"""
		subtotal = (self.valor_paquete_base or 0) + (self.valor_servicios_adicionales or 0)
		self.descuento_monto = subtotal * (self.descuento_porcentaje or 0) / 100
	
	def calculate_total(self):
		"""Calculate final total value"""
		subtotal = (self.valor_paquete_base or 0) + (self.valor_servicios_adicionales or 0)
		self.valor_total = subtotal - (self.descuento_monto or 0)
	
	def calculate_commission(self):
		"""Calculate SBC commission"""
		if self.porcentaje_comision and self.valor_total:
			self.comision_sbc = self.valor_total * self.porcentaje_comision / 100
		else:
			self.comision_sbc = 0
	
	def validate_dates(self):
		"""Validate date logic"""
		if self.fecha_inicio and self.fecha_fin:
			if getdate(self.fecha_fin) < getdate(self.fecha_inicio):
				frappe.throw("La fecha de fin no puede ser anterior a la fecha de inicio")
		
		if self.fecha_reserva and self.fecha_inicio:
			if getdate(self.fecha_inicio) < getdate(self.fecha_reserva):
				frappe.msgprint("Advertencia: La fecha de inicio es anterior a la fecha de reserva", 
					indicator='orange', alert=True)
	
	def set_commission_from_client(self):
		"""Get default commission from client if not set"""
		if not self.porcentaje_comision and self.cliente:
			client = frappe.get_doc("Cliente Turistico", self.cliente)
			if client.comision_estandar:
				self.porcentaje_comision = client.comision_estandar


@frappe.whitelist()
def get_client_info(client):
	"""Get client information for auto-filling fields"""
	if not client:
		return {}
	
	client_doc = frappe.get_doc("Cliente Turistico", client)
	return {
		"porcentaje_comision": client_doc.comision_estandar,
		"empleado_responsable": client_doc.empleado_asignado,
		"nacionalidad_grupo": client_doc.pais
	}


@frappe.whitelist()
def duplicate_reservation(source_name):
	"""Duplicate a reservation with a new ID"""
	from frappe.model.mapper import get_mapped_doc
	
	def set_missing_values(source, target):
		target.estado = "Borrador"
		target.fecha_confirmacion = None
		target.fecha_completada = None
		target.fecha_reserva = frappe.utils.today()
	
	target_doc = get_mapped_doc("Reserva Paquete", source_name, {
		"Reserva Paquete": {
			"doctype": "Reserva Paquete"
		},
		"Servicio Adicional Reserva": {
			"doctype": "Servicio Adicional Reserva"
		}
	}, None, set_missing_values)
	
	return target_doc
