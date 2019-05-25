from django.urls import path
from . import views

urlpatterns = [
    path('', views.songlistView, name='list'),
    path('<int:song_id>.html', views.songlistView, name='list')
]
