# -*- coding: utf-8 -*-
# Copyright (c) 2024, SBC Internationals and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def after_install():
	"""Setup tasks after app installation"""
	
	print("Setting up SBC CRM...")
	
	# Create default workspace
	create_workspace()
	
	# Setup default roles
	setup_roles()
	
	# Create sample data (optional)
	# create_sample_data()
	
	# Set default permissions
	setup_permissions()
	
	# Create custom fields if needed
	# create_custom_fields()
	
	print("SBC CRM setup completed!")


def create_workspace():
	"""Create SBC CRM workspace"""
	
	if frappe.db.exists("Workspace", "SBC CRM"):
		return
	
	workspace = frappe.get_doc({
		"doctype": "Workspace",
		"name": "SBC CRM",
		"title": "SBC CRM",
		"icon": "briefcase",
		"module": "SBC CRM",
		"is_standard": 0,
		"public": 1,
		"content": get_workspace_content()
	})
	
	workspace.insert(ignore_permissions=True)


def get_workspace_content():
	"""Get workspace HTML content"""
	
	return """
	[
		{
			"type": "Card Break",
			"data": {
				"col": 12
			}
		},
		{
			"type": "Card",
			"data": {
				"card_name": "Clientes",
				"col": 4
			}
		},
		{
			"type": "Card",
			"data": {
				"card_name": "Reservas",
				"col": 4
			}
		},
		{
			"type": "Card",
			"data": {
				"card_name": "Actividades",
				"col": 4
			}
		},
		{
			"type": "Card Break"
		},
		{
			"type": "Card",
			"data": {
				"card_name": "Reportes",
				"col": 12
			}
		}
	]
	"""


def setup_roles():
	"""Setup default roles for SBC CRM"""
	
	roles = [
		{
			"role_name": "Sales Master Manager",
			"desk_access": 1
		},
		{
			"role_name": "Sales User",
			"desk_access": 1
		}
	]
	
	for role_data in roles:
		if not frappe.db.exists("Role", role_data["role_name"]):
			role = frappe.get_doc({
				"doctype": "Role",
				"role_name": role_data["role_name"],
				"desk_access": role_data["desk_access"]
			})
			role.insert(ignore_permissions=True)


def setup_permissions():
	"""Setup default permissions"""
	
	# This is handled in DocType JSON files
	# Additional permission logic can be added here if needed
	pass


def create_sample_data():
	"""Create sample data for testing (optional)"""
	
	# Only create if no clients exist
	if frappe.db.count("Cliente Turistico") > 0:
		return
	
	# Create sample client
	sample_client = frappe.get_doc({
		"doctype": "Cliente Turistico",
		"nombre_empresa": "Hotel Example SA",
		"tipo_cliente": "Hotel",
		"categoria": "Potencial",
		"estrellas": "4 Estrellas",
		"contacto_principal": "Juan Pérez",
		"cargo": "Director de Compras",
		"email": "juan.perez@hotelexample.com",
		"telefono": "+34 912 345 678",
		"pais": "Spain",
		"ciudad": "Madrid",
		"comision_estandar": 15,
		"metodo_pago": "Transferencia Bancaria"
	})
	
	try:
		sample_client.insert(ignore_permissions=True)
		print(f"Created sample client: {sample_client.name}")
	except Exception as e:
		print(f"Could not create sample data: {str(e)}")
