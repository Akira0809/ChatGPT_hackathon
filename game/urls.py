from django.urls import path
from . import views, views_difficulty

app_name = 'game'
urlpatterns = [
    path("difficulty/", views_difficulty.difficulty, name="difficulty"),
    path("result/", views.result, name="result"),
]
