from django.core.cache import cache
from .models import Dish


def get_menu_for_cache():
    data = cache.get("menu")
    if data is None:
        data = list(
            Dish.objects.select_related("category")
            .prefetch_related("modifier_groups")
            .filter(is_active=True)
            .values()
        )
        cache.set("menu", data, timeout=3600)
    return data
