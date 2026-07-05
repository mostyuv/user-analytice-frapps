import frappe
from frappe.utils import getdate, add_days
import random

def after_install():
    if frappe.db.count("User Service Event") == 0:
        create_demo_data()

def create_demo_data():
    users = [
        {"name": "张伟", "region": "华东", "channel": "官网"},
        {"name": "李明", "region": "华南", "channel": "线下销售"},
        {"name": "王芳", "region": "华北", "channel": "合作伙伴"},
        {"name": "刘洋", "region": "西南", "channel": "官网"},
        {"name": "陈静", "region": "华东", "channel": "线下销售"},
        {"name": "赵强", "region": "海外", "channel": "其他"},
        {"name": "孙丽", "region": "华南", "channel": "官网"},
        {"name": "周杰", "region": "华北", "channel": "合作伙伴"},
        {"name": "吴敏", "region": "西南", "channel": "线下销售"},
        {"name": "郑伟", "region": "华东", "channel": "官网"},
        {"name": "黄琳", "region": "华南", "channel": "其他"},
        {"name": "杨帆", "region": "华北", "channel": "合作伙伴"},
        {"name": "许婷", "region": "西南", "channel": "官网"},
        {"name": "何军", "region": "海外", "channel": "线下销售"},
        {"name": "林娜", "region": "华东", "channel": "合作伙伴"},
        {"name": "罗敏", "region": "华南", "channel": "官网"},
        {"name": "郭磊", "region": "华北", "channel": "合作伙伴"},
        {"name": "梁婷", "region": "西南", "channel": "线下销售"},
        {"name": "宋涛", "region": "海外", "channel": "其他"},
        {"name": "韩雪", "region": "华东", "channel": "官网"},
        {"name": "唐浩", "region": "华南", "channel": "线下销售"},
        {"name": "邓丽", "region": "华北", "channel": "官网"},
        {"name": "冯刚", "region": "西南", "channel": "合作伙伴"},
        {"name": "曹琳", "region": "海外", "channel": "其他"},
        {"name": "彭飞", "region": "华东", "channel": "官网"},
        {"name": "蒋敏", "region": "华南", "channel": "合作伙伴"},
        {"name": "沈涛", "region": "华北", "channel": "线下销售"},
        {"name": "苏婷", "region": "西南", "channel": "官网"},
        {"name": "卢伟", "region": "海外", "channel": "其他"},
        {"name": "蔡雪", "region": "华东", "channel": "线下销售"},
    ]

    plans = ["基础版", "专业版", "企业版"]
    plan_prices = {"基础版": 99, "专业版": 299, "企业版": 999}

    today = getdate()
    random.seed(42)

    for i in range(90):
        event_date = add_days(today, -i)
        num_events = random.randint(2, 5)

        for j in range(num_events):
            idx = random.randint(0, len(users) - 1)
            user = users[idx]
            plan = random.choice(plans)

            rand = random.random()
            if rand < 0.05:
                event_type = "流失"
                is_active = 0
                revenue = 0
            elif rand < 0.15:
                event_type = "续费"
                is_active = 1
                revenue = plan_prices[plan]
            else:
                event_type = "开通"
                is_active = 1
                revenue = plan_prices[plan]

            try:
                frappe.get_doc({
                    "doctype": "User Service Event",
                    "user_name": user["name"],
                    "service_plan": plan,
                    "event_type": event_type,
                    "event_date": event_date,
                    "channel": user["channel"],
                    "region": user["region"],
                    "revenue": revenue,
                    "is_active": is_active,
                    "remarks": "演示数据"
                }).insert(ignore_permissions=True)
            except Exception as e:
                frappe.log_error(
                    message=f"Demo data insert failed: {user['name']} on {event_date}: {str(e)}",
                    title="Demo Data Error"
                )

    frappe.db.commit()
