frappe.views.calendar["Actividad Comercial"] = {
    field_map: {
        "start": "fecha_hora_inicio",
        "end": "fecha_hora_fin",
        "id": "name",
        "title": "titulo",
        "status": "estado",
        "allDay": "todo_el_dia"
    },
    gantt: false,
    get_events_method: "sbc_cr34.sbc_crm.doctype.actividad_comercial.actividad_comercial.get_events"
};
