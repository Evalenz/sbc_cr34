# -*- coding: utf-8 -*-
# Copyright (c) 2024, SBC Internationals and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def get_notification_config():
	"""Configure desk notifications for SBC CRM"""
	
	return {
		"for_doctype": {
			"Reserva Paquete": {
				"status": "estado"
			},
			"Actividad Comercial": {
				"status": "estado"
			},
			"Cliente Turistico": {
				"status": "categoria"
			}
		},
		"for_module_doctypes": {
			"SBC CRM": "badge-primary"
		},
		"for_other_doctypes": {}
	}


def get_open_count(doctype, name, items=[]):
	"""Get count of open/pending items"""
	
	if doctype == "Cliente Turistico":
		# Count pending reservations for client
		return frappe.db.count("Reserva Paquete", {
			"cliente": name,
			"estado": ["in", ["Pendiente", "Confirmada", "En Proceso"]],
			"docstatus": 1
		})
	
	elif doctype == "Reserva Paquete":
		# Count pending activities for reservation
		return frappe.db.count("Actividad Comercial", {
			"reserva_relacionada": name,
			"estado": ["in", ["Programada", "En Curso"]]
		})
	
	return 0
