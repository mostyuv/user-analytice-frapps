import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def get_dashboard_data(days=30):
    from frappe.utils import getdate, add_days

    days = int(days)
    end_date = getdate()
    start_date = add_days(end_date, -days + 1)
    prev_start = add_days(start_date, -days)
    prev_end = add_days(end_date, -days)

    kpi_rows = frappe.db.sql("""
        SELECT
            SUM(CASE WHEN event_type = '开通' AND event_date BETWEEN %s AND %s THEN 1 ELSE 0 END) as new_activations,
            SUM(CASE WHEN event_type = '流失' AND event_date BETWEEN %s AND %s THEN 1 ELSE 0 END) as churned_users,
            SUM(CASE WHEN event_type IN ('开通', '续费') AND event_date BETWEEN %s AND %s THEN revenue ELSE 0 END) as revenue,
            SUM(CASE WHEN event_type = '开通' AND event_date BETWEEN %s AND %s THEN 1 ELSE 0 END) as prev_activations,
            SUM(CASE WHEN event_type = '流失' AND event_date BETWEEN %s AND %s THEN 1 ELSE 0 END) as prev_churns,
            SUM(CASE WHEN event_type IN ('开通', '续费') AND event_date BETWEEN %s AND %s THEN revenue ELSE 0 END) as prev_revenue
        FROM `tabUser Service Event`
    """, (
        start_date, end_date,
        start_date, end_date,
        start_date, end_date,
        prev_start, prev_end,
        prev_start, prev_end,
        prev_start, prev_end
    ))[0]

    new_activations = int(kpi_rows[0] or 0)
    churned_users = int(kpi_rows[1] or 0)
    revenue = float(kpi_rows[2] or 0)
    prev_activations = int(kpi_rows[3] or 0)
    prev_churns = int(kpi_rows[4] or 0)
    prev_revenue = float(kpi_rows[5] or 0)

    active_users = frappe.db.count("User Service Event", filters={"is_active": 1})

    prev_active_start = add_days(end_date, -days * 2)
    prev_active_end = add_days(end_date, -days)
    prev_active_users = frappe.db.sql("""
        SELECT COUNT(DISTINCT user_name)
        FROM `tabUser Service Event`
        WHERE is_active = 1 AND event_date BETWEEN %s AND %s
    """, (prev_active_start, prev_active_end))[0][0]

    def calc_change(current, prev):
        return round(((current - prev) / prev) * 100, 1) if prev > 0 else 0

    trend_rows = frappe.db.sql("""
        SELECT
            DATE(event_date) as date,
            SUM(CASE WHEN event_type = '开通' THEN 1 ELSE 0 END) as activations,
            SUM(CASE WHEN event_type = '流失' THEN 1 ELSE 0 END) as churns
        FROM `tabUser Service Event`
        WHERE event_date BETWEEN %s AND %s
        GROUP BY DATE(event_date)
        ORDER BY date
    """, (start_date, end_date), as_dict=True)

    trend_map = {str(r.date): r for r in trend_rows}
    trend_dates = []
    trend_activations = []
    trend_churns = []
    for i in range(days):
        d = add_days(start_date, i)
        key = str(d)
        trend_dates.append(d.strftime("%m-%d"))
        if key in trend_map:
            trend_activations.append(int(trend_map[key].activations or 0))
            trend_churns.append(int(trend_map[key].churns or 0))
        else:
            trend_activations.append(0)
            trend_churns.append(0)

    region_data = frappe.db.sql(
        "SELECT region, COUNT(*) as cnt FROM `tabUser Service Event` WHERE is_active = 1 GROUP BY region ORDER BY cnt DESC"
    )
    region_labels = [r[0] for r in region_data]
    region_values = [r[1] for r in region_data]

    plan_data = frappe.db.sql(
        "SELECT service_plan, COUNT(*) as cnt FROM `tabUser Service Event` WHERE is_active = 1 GROUP BY service_plan ORDER BY cnt DESC"
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
        as_dict=True
    )

    return {
        "kpi": {
            "active_users": active_users,
            "new_activations": new_activations,
            "churned_users": churned_users,
            "revenue": round(revenue, 2),
            "active_users_change": calc_change(active_users, prev_active_users),
            "new_activations_change": calc_change(new_activations, prev_activations),
            "churned_users_change": calc_change(churned_users, prev_churns),
            "revenue_change": calc_change(revenue, prev_revenue)
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
def export_csv(days=30):
    import csv
    from io import StringIO
    from frappe.utils import getdate, add_days

    days = int(days)
    end_date = getdate()
    start_date = add_days(end_date, -days)

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
