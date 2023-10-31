from django.urls import path

from . import views


app_name = 'about'

urlpatterns = [
    path('me/',
         views.AboutAuthorView.as_view(),
         name='author'),
    path('outfit/',
         views.AboutOutfitView.as_view(),
         name='outfit'),
    path('navigation/',
         views.AboutnavigationView.as_view(),
         name='navigation'),
]
