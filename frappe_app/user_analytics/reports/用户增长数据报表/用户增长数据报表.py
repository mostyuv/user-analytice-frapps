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

        rows = frappe.db.sql("""
            SELECT
                DATE(event_date) as date,
                SUM(CASE WHEN event_type = '开通' THEN 1 ELSE 0 END) as activations,
                SUM(CASE WHEN event_type = '流失' THEN 1 ELSE 0 END) as churns,
                SUM(CASE WHEN event_type IN ('开通', '续费') THEN revenue ELSE 0 END) as revenue
            FROM `tabUser Service Event`
            WHERE event_date BETWEEN %s AND %s
            GROUP BY DATE(event_date)
            ORDER BY date
        """, (start_date, end_date), as_dict=True)

        row_map = {str(r.date): r for r in rows}

        for i in range(days):
            current_date = add_days(start_date, i)
            date_key = str(current_date)

            if date_key in row_map:
                r = row_map[date_key]
                activations = int(r.activations or 0)
                churns = int(r.churns or 0)
                revenue = flt(r.revenue or 0, 2)
            else:
                activations = 0
                churns = 0
                revenue = 0

            data.append({
                "date": current_date,
                "activations": activations,
                "churns": churns,
                "net_growth": activations - churns,
                "revenue": revenue
            })

    return columns, data
