import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def get_dashboard_data(days=30):
    from datetime import datetime, timedelta
    from frappe.utils import getdate, add_days

    end_date = getdate()
    start_date = add_days(end_date, -int(days) + 1)
    prev_start = add_days(start_date, -int(days))
    prev_end = add_days(end_date, -int(days))

    new_activations = frappe.db.sql(
        "SELECT COUNT(*) FROM `tabUser Service Event` WHERE event_type = %s AND event_date BETWEEN %s AND %s",
        ("开通", start_date, end_date)
    )[0][0]

    churned_users = frappe.db.sql(
        "SELECT COUNT(*) FROM `tabUser Service Event` WHERE event_type = %s AND event_date BETWEEN %s AND %s",
        ("流失", start_date, end_date)
    )[0][0]

    revenue = frappe.db.sql(
        "SELECT COALESCE(SUM(revenue), 0) FROM `tabUser Service Event` WHERE event_type IN (%s, %s) AND event_date BETWEEN %s AND %s",
        ("开通", "续费", start_date, end_date)
    )[0][0]

    active_users = frappe.db.sql(
        "SELECT COUNT(*) FROM `tabUser Service Event` WHERE is_active = 1",
        ()
    )[0][0]

    prev_activations = frappe.db.sql(
        "SELECT COUNT(*) FROM `tabUser Service Event` WHERE event_type = %s AND event_date BETWEEN %s AND %s",
        ("开通", prev_start, prev_end)
    )[0][0]

    prev_churns = frappe.db.sql(
        "SELECT COUNT(*) FROM `tabUser Service Event` WHERE event_type = %s AND event_date BETWEEN %s AND %s",
        ("流失", prev_start, prev_end)
    )[0][0]

    prev_revenue = frappe.db.sql(
        "SELECT COALESCE(SUM(revenue), 0) FROM `tabUser Service Event` WHERE event_type IN (%s, %s) AND event_date BETWEEN %s AND %s",
        ("开通", "续费", prev_start, prev_end)
    )[0][0]

    new_activations_change = round(((new_activations - prev_activations) / prev_activations) * 100, 1) if prev_activations > 0 else 0
    churned_users_change = round(((churned_users - prev_churns) / prev_churns) * 100, 1) if prev_churns > 0 else 0
    revenue_change = round(((revenue - prev_revenue) / prev_revenue) * 100, 1) if prev_revenue > 0 else 0

    trend_dates = []
    trend_activations = []
    trend_churns = []

    for i in range(int(days)):
        d = add_days(start_date, i)
        trend_dates.append(d.strftime("%m-%d"))
        trend_activations.append(frappe.db.sql(
            "SELECT COUNT(*) FROM `tabUser Service Event` WHERE event_type = %s AND event_date = %s",
            ("开通", d)
        )[0][0])
        trend_churns.append(frappe.db.sql(
            "SELECT COUNT(*) FROM `tabUser Service Event` WHERE event_type = %s AND event_date = %s",
            ("流失", d)
        )[0][0])

    region_data = frappe.db.sql(
        "SELECT region, COUNT(*) as cnt FROM `tabUser Service Event` WHERE is_active = 1 GROUP BY region ORDER BY cnt DESC",
        ()
    )
    region_labels = [r[0] for r in region_data]
    region_values = [r[1] for r in region_data]

    plan_data = frappe.db.sql(
        "SELECT service_plan, COUNT(*) as cnt FROM `tabUser Service Event` WHERE is_active = 1 GROUP BY service_plan ORDER BY cnt DESC",
        ()
    )
    plan_labels = [p[0] for p in plan_data]
    plan_values = [p[1] for p in plan_data]

    channel_data = frappe.db.sql(
        "SELECT channel, COUNT(*) as cnt FROM `tabUser Service Event` WHERE event_type = %s AND event_date BETWEEN %s AND %s GROUP BY channel ORDER BY cnt DESC",
        ("开通", start_date, end_date)
    )
    channel_labels = [ch[0] for ch in channel_data]
    channel_values = [ch[1] for ch in channel_data]

    recent_events = frappe.db.sql(
        "SELECT user_name, service_plan, event_type, event_date FROM `tabUser Service Event` ORDER BY event_date DESC LIMIT 10",
        (),
        as_dict=True
    )

    return {
        "kpi": {
            "active_users": active_users,
            "new_activations": new_activations,
            "churned_users": churned_users,
            "revenue": round(float(revenue), 2),
            "active_users_change": 0,
            "new_activations_change": new_activations_change,
            "churned_users_change": churned_users_change,
            "revenue_change": revenue_change
        },
        "trend": {
            "dates": trend_dates,
            "activations": trend_activations,
            "churns": trend_churns
        },
        "region_distribution": {
            "labels": region_labels,
            "values": region_values
        },
        "plan_distribution": {
            "labels": plan_labels,
            "values": plan_values
        },
        "channel_distribution": {
            "labels": channel_labels,
            "values": channel_values
        },
        "recent_events": recent_events
    }

@frappe.whitelist(allow_guest=True)
def export_csv():
    import csv
    from io import StringIO
    from frappe.utils import getdate, add_days

    end_date = getdate()
    start_date = add_days(end_date, -30)

    events = frappe.db.sql(
        "SELECT user_name, service_plan, event_type, event_date, region, channel, revenue, is_active FROM `tabUser Service Event` WHERE event_date BETWEEN %s AND %s",
        (start_date, end_date),
        as_dict=True
    )

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["用户姓名", "服务套餐", "事件类型", "事件日期", "地区", "渠道", "收入", "是否活跃"])

    for event in events:
        writer.writerow([
            event.get("user_name", ""),
            event.get("service_plan", ""),
            event.get("event_type", ""),
            event.get("event_date", ""),
            event.get("region", ""),
            event.get("channel", ""),
            event.get("revenue", 0),
            "是" if event.get("is_active") else "否"
        ])

    return output.getvalue()

def get_context(context):
    context.no_cache = True
    context.title = _("用户增长数据大屏")