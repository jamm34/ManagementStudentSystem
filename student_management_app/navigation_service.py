import json

from django.core.cache import cache

from student_management_app.models import NavigationConfig
from student_management_app.sidebar_config import SIDEBAR_CONFIG


def _default_role_config(user_type):
    return SIDEBAR_CONFIG.get(user_type, {})


def get_role_navigation_config(user_type):
    default_config = _default_role_config(user_type)
    if not default_config:
        return {}

    cache_key = f'sidebar_role_config:{user_type}'
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    resolved = default_config

    try:
        db_config = NavigationConfig.objects.filter(role=user_type, is_active=True).first()
        if db_config and db_config.menu_json:
            parsed_menu = json.loads(db_config.menu_json)
            if isinstance(parsed_menu, list):
                resolved = {
                    'brand': db_config.brand or default_config.get('brand', ''),
                    'home_url_name': db_config.home_url_name or default_config.get('home_url_name', ''),
                    'menu': parsed_menu,
                }
    except Exception:
        resolved = default_config

    cache.set(cache_key, resolved, 300)
    return resolved
