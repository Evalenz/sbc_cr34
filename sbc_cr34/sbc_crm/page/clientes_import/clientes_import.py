# Copyright (c) 2024, SBC Internationals
# License: MIT

import frappe


def get_context(context):
	"""Contexto para la página clientes_import"""
	context.update({
		"title": "Gestión de Clientes",
		"description": "Importar y exportar clientes desde CSV"
	})
	return context
