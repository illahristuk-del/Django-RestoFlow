from django.urls import path
from .views import MenuView

urlpatterns = [path("menu/get_cache_menu/", MenuView.as_view(), name="get_cached_menu")]
