from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from recipes import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about_author/', views.about_author, name='about_author'),
    path('follows/', views.follow_index, name='follows'),
    path('create_recipe/', views.create_recipe, name='create_recipe'),
    path('favorites/', views.favorites, name='favorites'),
    path('shoplist/', views.shoplist, name='shoplist'),
    path(
        'shoplist_download/',
        views.shoplist_download,
        name='shoplist_download'),
    path('<str:username>/', views.profile, name='profile'),
    path('<int:recipe_id>/delete/', views.delete_recipe, name='delete_recipe'),
    path('<str:username>/<int:recipe_id>/change/', views.change_recipe,
         name='change_recipe'),
    path('<str:username>/<int:recipe_id>/', views.recipe_view, name='recipe'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
