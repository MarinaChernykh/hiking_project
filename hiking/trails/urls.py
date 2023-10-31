from django.urls import path

from . import views


app_name = 'trails'

urlpatterns = [
    path('region/<slug:slug_region>/',
         views.region_detail,
         name='region_detail'),
    path('trails/<slug:slug_region>/all/',
         views.trails_list,
         name='region_trails_list'),
    path('trails/<slug:slug_trail>/comments/',
         views.comments_list,
         name='comments_list'),
    path('trails/<slug:slug_trail>/comment/',
         views.add_comment,
         name='add_comment'),
    path('trails/<slug:slug_trail>/',
         views.trail_detail,
         name='trail_detail'),
    path('trails/',
         views.trails_list,
         name='trails_list'),
    path('search/', views.trails_search, name='trails_search'),
    path('', views.index, name='index'),
]
