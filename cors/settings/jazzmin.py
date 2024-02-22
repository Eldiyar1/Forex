from django.utils.translation import gettext_lazy as _


JAZZMIN_SETTINGS = {
    "site_title": "Forex",
    "site_header": "Forex",
    "site_logo_classes": "img-circle",
    "site_brand": _("Admin site"),
    "welcome_sign": _("Welcome to Forex"),
    "copyright": "Forex",
    "search_model": ["auth.User", "auth.Group", "products.Product"],
    "show_ui_builder": True,
    "topmenu_links": [
        {"name": _("Home"), "url": "admin:index", "permissions": ["auth.view_user"]},
        {"app": "Forex"},
        {"model": "auth.User"},
        {"name": "Support", "url": "https://t.me/elldiyar", "new_window": True},
    ],
    "default_icon_parents": "fas fa-circle",
    "default_icon_children": "fas fa-dot-circle",
    "show_sidebar": True,
    "navigation_expanded": True,
    "changeform_format": "horizontal_tabs",
    "language_chooser": True,
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
    "icons": {
        "courses.Course": "fas fa-list-alt",
        "courses.Lecture": "fas fa-solid fa-video",
        "courses.Review": "fas fa-solid fa-comment",
        "users.User": "fas fa-user",
        "auth.Group": "fas fa-users"
    },
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-warning",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": True,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success",
    },
    "actions_sticky_top": True,
}
