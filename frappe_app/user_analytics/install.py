import frappe
from frappe.utils import getdate, add_days

def after_install():
    if frappe.db.count("User Service Event") == 0:
        create_demo_data()

def create_demo_data():
    from datetime import datetime
    
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
    ]
    
    plans = ["基础版", "专业版", "企业版"]
    plan_prices = {"基础版": 99, "专业版": 299, "企业版": 999}
    
    today = getdate()
    
    for i in range(30):
        event_date = add_days(today, -i)
        num_events = 1 if i > 20 else (2 if i > 10 else 3)
        
        for j in range(num_events):
            idx = (i * num_events + j) % len(users)
            user = users[idx]
            plan = plans[(i + j) % 3]
            
            if i in [5, 18] and j == 0:
                event_type = "流失"
                is_active = 0
                revenue = 0
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
            except Exception:
                pass
    
    frappe.db.commit()