app_name = "sbc_cr34"
app_title = "sbc_crm"
app_publisher = "SBC Internationals"
app_description = "CRM personalizado para SBC Internationals"
app_email = "sbcinternational@protonmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
add_to_apps_screen = [
	{
		"name": "sbc_cr34",
		"logo": "/assets/sbc_cr34/logo.png",
		"title": "SBC CRM",
		"route": "/app/sbc-crm",
		"has_permission": "sbc_cr34.api.permission.has_app_permission"
	}
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# COMENTADO: No usar build, cargar directamente
# app_include_css = "/assets/sbc_cr34/css/sbc_cr34.css"
# app_include_js = "/assets/sbc_cr34/js/sbc_cr34.js"

# include js, css files in header of web template
# web_include_css = "/assets/sbc_cr34/css/sbc_cr34.css"
# web_include_js = "/assets/sbc_cr34/js/sbc_cr34.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "sbc_cr34/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
page_js = {
	"clientes_import": "public/js/clientes_import.js"
}

# include js in doctype views
# Los archivos JS se cargarán directamente sin compilación
doctype_js = {
	"Cliente Turistico": "public/js/cliente_turistico.js",
	"Reserva Paquete": "public/js/reserva_paquete.js",
	"Actividad Comercial": "public/js/actividad_comercial.js"
}

# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}

# Calendar views for activities
doctype_calendar_js = {
	"Actividad Comercial": "public/js/actividad_comercial_calendar.js"
}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "sbc_cr34/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
role_home_page = {
	"Sales User": "/app/sbc-crm",
	"Sales Master Manager": "/app/sbc-crm"
}

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "sbc_cr34.utils.jinja_methods",
# 	"filters": "sbc_cr34.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "sbc_cr34.install.before_install"
after_install = "sbc_cr34.setup.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "sbc_cr34.uninstall.before_uninstall"
# after_uninstall = "sbc_cr34.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "sbc_cr34.utils.before_app_install"
# after_app_install = "sbc_cr34.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "sbc_cr34.utils.before_app_uninstall"
# after_app_uninstall = "sbc_cr34.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

notification_config = "sbc_cr34.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

permission_query_conditions = {
	"Reserva Paquete": "sbc_cr34.sbc_crm.doctype.reserva_paquete.reserva_paquete.get_permission_query_conditions",
	"Actividad Comercial": "sbc_cr34.sbc_crm.doctype.actividad_comercial.actividad_comercial.get_permission_query_conditions"
}

has_permission = {
	"Reserva Paquete": "sbc_cr34.sbc_crm.doctype.reserva_paquete.reserva_paquete.has_permission",
	"Actividad Comercial": "sbc_cr34.sbc_crm.doctype.actividad_comercial.actividad_comercial.has_permission"
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Reserva Paquete": {
		"validate": "sbc_cr34.sbc_crm.doctype.reserva_paquete.reserva_paquete.validate",
		"on_submit": "sbc_cr34.sbc_crm.doctype.reserva_paquete.reserva_paquete.on_submit",
		"on_update_after_submit": "sbc_cr34.sbc_crm.doctype.reserva_paquete.reserva_paquete.on_update_after_submit"
	},
	"Actividad Comercial": {
		"validate": "sbc_cr34.sbc_crm.doctype.actividad_comercial.actividad_comercial.validate",
		"on_update": "sbc_cr34.sbc_crm.doctype.actividad_comercial.actividad_comercial.on_update"
	},
	"Cliente Turistico": {
		"validate": "sbc_cr34.sbc_crm.doctype.cliente_turistico.cliente_turistico.validate"
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"daily": [
		"sbc_cr34.tasks.send_daily_activity_reminder",
		"sbc_cr34.tasks.update_client_categories"
	],
	"weekly": [
		"sbc_cr34.tasks.send_weekly_sales_report"
	],
	"monthly": [
		"sbc_cr34.tasks.generate_monthly_analytics"
	]
}

# Testing
# -------

# before_tests = "sbc_cr34.install.before_tests"

# Extend DocType Class
# ------------------------------
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "sbc_cr34.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------

override_whitelisted_methods = {
	"frappe.desk.reportview.get": "sbc_cr34.overrides.get"
}

# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
override_doctype_dashboards = {
	"Cliente Turistico": "sbc_cr34.sbc_crm.doctype.cliente_turistico.cliente_turistico_dashboard.get_data",
	"Reserva Paquete": "sbc_cr34.sbc_crm.doctype.reserva_paquete.reserva_paquete_dashboard.get_data"
}

# exempt linked doctypes from being automatically cancelled
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["sbc_cr34.utils.before_request"]
# after_request = ["sbc_cr34.utils.after_request"]

# Job Events
# ----------
# before_job = ["sbc_cr34.utils.before_job"]
# after_job = ["sbc_cr34.utils.after_job"]

# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "Cliente Turistico",
		"filter_by": "empleado_asignado",
		"redact_fields": ["email", "telefono", "telefono_movil", "whatsapp"],
		"partial": 1
	},
	{
		"doctype": "Actividad Comercial",
		"filter_by": "empleado_responsable",
		"partial": 1
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"sbc_cr34.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

# Global Search
# -------------
# DocTypes to include in global search
global_search_doctypes = {
	"Cliente Turistico": {
		"search_fields": "nombre_empresa,contacto_principal,email,ciudad",
		"order_by": "nombre_empresa"
	},
	"Reserva Paquete": {
		"search_fields": "titulo_reserva,destino,cliente",
		"order_by": "fecha_reserva desc"
	}
}

# Custom Links
# ------------
# Add custom links to the desktop
# desktop_icons = {
# 	"Cliente Turistico": "customer",
# 	"Reserva Paquete": "vacation",
# 	"Actividad Comercial": "calendar"
# }

# Website
# --------
# Custom website routes
# website_route_rules = [
# 	{"from_route": "/sbc-crm/<path:app_path>", "to_route": "sbc-crm"},
# ]

# Pages
# ------
# Register custom pages
fixtures = [
	{
		"doctype": "Page",
		"name": "clientes-import"
	}
]

# Fixtures
# --------
# Fixtures to export default data
fixtures = [
	{
		"doctype": "Custom Field",
		"filters": [
			["name", "in", [
				"Cliente Turistico-custom_field",
				"Reserva Paquete-custom_field"
			]]
		]
	},
	{
		"doctype": "Property Setter",
		"filters": [
			["doc_type", "in", [
				"Cliente Turistico",
				"Reserva Paquete",
				"Actividad Comercial"
			]]
		]
	}
]
