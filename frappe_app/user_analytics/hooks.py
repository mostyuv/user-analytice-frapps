from . import __version__

app_name = "user_analytics"
app_title = "用户增长分析"
app_publisher = "Developer"
app_description = "用户服务开通/流失信息管理与数据大屏展示"
app_version = __version__
app_icon = "octicon octicon-bar-chart"
app_color = "#00d4ff"
app_email = "support@example.com"
app_license = "MIT"

doctype_list = [
    {
        "name": "User Service Event",
        "module": "User Analytics",
        "custom": 1,
        "fields": [],
        "permissions": [],
    }
]

report_list = [
    {
        "doctype": "User Service Event",
        "name": "用户增长数据报表",
        "module": "User Analytics",
        "report_type": "Script Report",
        "is_standard": "Yes",
        "ref_doctype": "User Service Event",
    }
]

page_list = [
    {
        "name": "user-growth-dashboard",
        "title": "用户增长数据大屏",
        "module": "User Analytics",
        "page_type": "Standard",
    }
]

web_pages = [
    {
        "route": "/user-growth-dashboard",
        "page": "user-growth-dashboard",
    }
]

install_before = []
install_after = []

fixtures = []

after_install = "user_analytics.install.after_install"