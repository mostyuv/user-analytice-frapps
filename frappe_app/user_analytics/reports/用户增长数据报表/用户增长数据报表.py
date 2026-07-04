import frappe
from frappe import _
from frappe.utils import flt, getdate, add_days

def execute(filters=None):
    columns = [
        {
            "label": _("日期"),
            "fieldname": "date",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "label": _("开通数"),
            "fieldname": "activations",
            "fieldtype": "Int",
            "width": 100,
            "align": "right"
        },
        {
            "label": _("流失数"),
            "fieldname": "churns",
            "fieldtype": "Int",
            "width": 100,
            "align": "right"
        },
        {
            "label": _("净增长"),
            "fieldname": "net_growth",
            "fieldtype": "Int",
            "width": 100,
            "align": "right"
        },
        {
            "label": _("收入"),
            "fieldname": "revenue",
            "fieldtype": "Currency",
            "width": 120,
            "align": "right"
        }
    ]

    data = []
    if filters:
        days = int(filters.get("days", 30))
        end_date = getdate()
        start_date = add_days(end_date, -days + 1)

        for i in range(days):
            current_date = add_days(start_date, i)
            date_str = current_date.strftime("%Y-%m-%d")

            activations = frappe.db.count(
                "User Service Event",
                filters={"event_type": "开通", "event_date": date_str}
            )

            churns = frappe.db.count(
                "User Service Event",
                filters={"event_type": "流失", "event_date": date_str}
            )

            revenue = frappe.db.sum(
                "User Service Event",
                "revenue",
                filters={
                    "event_type": ["in", ["开通", "续费"]],
                    "event_date": date_str
                }
            ) or 0

            data.append({
                "date": date_str,
                "activations": activations,
                "churns": churns,
                "net_growth": activations - churns,
                "revenue": flt(revenue, 2)
            })

    return columns, data