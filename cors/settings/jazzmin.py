from django.utils.translation import gettext_lazy as _


JAZZMIN_SETTINGS = {
    "site_title": "Forex",
    "site_header": "Forex",
    "site_logo_classes": "img-circle",
    "site_brand": _("Админ панель"),
    "welcome_sign": "Добро пожаловать в Forex",
    "copyright": "Forex",
    "search_model": ["auth.User", "auth.Group", "products.Product"],
    "show_ui_builder": True,
    "topmenu_links": [
        {"name": _("Главная"), "url": "admin:index", "permissions": ["auth.view_user"]},
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
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": True,
    "sidebar_disable_expand": True,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": True,
    "sidebar_nav_flat_style": True,
    "theme": "darkly",
    "dark_mode_theme": "cyborg",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-primary"
    },
    "actions_sticky_top": True
}
