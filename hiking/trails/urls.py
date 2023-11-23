from django.urls import path

from . import views


app_name = 'trails'

urlpatterns = [
    path('region/<slug:slug_region>/',
         views.region_detail,
         name='region_detail'),
    path('trails/favorite/',
         views.favorite_list,
         name='favorite_list'),
    path('trails/<slug:slug_region>/all/',
         views.trails_list,
         name='region_trails_list'),
    path('trails/<slug:slug_trail>/comments/',
         views.comments_list,
         name='comments_list'),
    path('trails/<slug:slug_trail>/add_comment/',
         views.add_comment,
         name='add_comment'),
    path('trails/<slug:slug_trail>/edit_comment/<int:pk>/',
         views.edit_comment,
         name='edit_comment'),
    path('trails/<slug:slug_trail>/delete_comment/<int:pk>/',
         views.delete_comment,
         name='delete_comment'),
    path('trails/<slug:slug_trail>/',
         views.trail_detail,
         name='trail_detail'),
    path('trails/<slug:slug_trail>/add_favorite/',
         views.add_favorite,
         name='add_favorite'),
    path('trails/<slug:slug_trail>/delete_favorite/',
         views.delete_favorite,
         name='delete_favorite'),
    path('trails/',
         views.trails_list,
         name='trails_list'),
    path('search/', views.trails_search, name='trails_search'),
    path('', views.index, name='index'),
]
