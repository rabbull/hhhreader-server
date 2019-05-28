from django.urls import path

from trans import views

urlpatterns = [
    path('word/<str:word>', views.query_word, name='word_query'),
    path('paragraph/', views.query_paragraph, name='paragraph_query'),
    path('<str:user_openid>/marks/<str:word>', views.mark, name='mark'),
    path('<str:user_openid>/all/', views.query_all_marked_word, name='all_marked'),
]
