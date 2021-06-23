from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.urls import path

from recipes import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about_author/', views.about_author, name='about_author'),
    path('follows/', views.follow_index, name='follows'),
    path('favorites/', views.favorites, name='favorites'),
    path('shoplist/', views.shoplist, name='shoplist'),
    path('shoplist_download/',
         views.shoplist_download,
         name='shoplist_download'),
    path('create_recipe/',
         login_required(views.RecipeCreateChange.as_view()),
         name='create_recipe'),
    path('<int:recipe_id>/delete/', views.delete_recipe, name='delete_recipe'),
    path('<str:username>/<int:recipe_id>/', views.recipe_view, name='recipe'),
    path('<str:username>/<int:recipe_id>/change/',
         login_required(views.RecipeCreateChange.as_view()),
         name='change_recipe'),
    path('<str:username>/', views.profile, name='profile'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
