from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500

urlpatterns = [
    path("admin_panel/", admin.site.urls),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("api/", include('api.urls')),
    path("", include("recipes.urls")),
]


handler404 = "recipes.views.page_not_found"  # noqa
handler500 = "recipes.views.server_error"  # noqa
