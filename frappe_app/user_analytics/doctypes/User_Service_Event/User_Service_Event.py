import frappe
from frappe.model.document import Document

class UserServiceEvent(Document):
    def validate(self):
        if self.event_type == "流失" and self.revenue and self.revenue != 0:
            frappe.throw("流失事件的收入必须为 0")

        if self.event_type == "续费" and not self.is_active:
            frappe.throw("续费事件的用户必须为活跃状态")

    def before_save(self):
        if self.event_type == "流失":
            self.is_active = 0
            self.revenue = 0
        elif self.event_type in ["开通", "续费"]:
            self.is_active = 1
