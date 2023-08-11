from django.urls import path
from . import views, views_difficulty

app_name = 'game'
urlpatterns = [
    path("", views.game, name="game"),
    path("difficulty/", views_difficulty.difficulty, name="difficulty"),
]
