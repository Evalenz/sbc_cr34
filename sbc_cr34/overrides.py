"""Overrides for Frappe methods"""

import frappe


@frappe.whitelist()
def get(doctype, start, page_length, filters, fields, order_by, with_comment_count=False, group_by="", unique=None, count=False, **kwargs):
	"""Override for frappe.desk.reportview.get
	
	This function wraps the original frappe.desk.reportview.get method
	to add custom functionality for the SBC CRM application.
	"""
	from frappe.desk.reportview import get as frappe_get
	
	# Call the original Frappe method
	return frappe_get(
		doctype=doctype,
		start=start,
		page_length=page_length,
		filters=filters,
		fields=fields,
		order_by=order_by,
		with_comment_count=with_comment_count,
		group_by=group_by,
		unique=unique,
		count=count,
		**kwargs
	)
