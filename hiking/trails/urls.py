from django.urls import path

from . import views


app_name = 'trails'

urlpatterns = [
    path('region/<slug:region>/', views.region_detail, name='region_detail'),
    path('trails/<slug:region>/all/', views.region_trails_list, name='region_trails_list'),
    path('trails/<slug:trail>/', views.trail_detail, name='trail_detail'),
    path('trails/', views.trails_list, name='trails_list'),
    path('', views.index, name='index'),
]
