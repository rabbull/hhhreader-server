from django.urls import path

from trans import views

urlpatterns = [
    path('word/<str:word>', views.query_word, name='word_query'),
]
