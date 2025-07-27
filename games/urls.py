from django.urls import path
from games import views
from games.views import GameListView, GameDetailView

app_name = 'games'

urlpatterns = [
    path('', GameListView.as_view(), name='game_list'),
    path('<int:pk>/', GameDetailView.as_view(), name='game_detail'),
    path('create/', views.GameCreateView.as_view(), name='game_create'),
    path('<int:pk>/edit/', views.GameUpdateView.as_view(), name='game_edit'),
    path('<int:pk>/delete/', views.GameDeleteView.as_view(), name='game_delete'),
    path('<int:game_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
]
