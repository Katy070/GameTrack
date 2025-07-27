from django.urls import path
from . import views

app_name = 'tracking'

urlpatterns = [
    path('start/<int:game_id>/', views.start_tracking, name='start_tracking'),
    path('stop/<int:game_id>/', views.stop_tracking, name='stop_tracking'),
]
