import frappe
from frappe.model.document import Document

class UserServiceEvent(Document):
    def before_save(self):
        if self.event_type == "流失":
            self.is_active = 0
        elif self.event_type in ["开通", "续费"]:
            self.is_active = 1