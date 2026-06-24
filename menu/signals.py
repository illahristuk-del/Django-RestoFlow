from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import Dish

@receiver(post_save, sender=Dish)
def invalidate_menu_cache(sender, **kwargs):
    cache.delete('menu')