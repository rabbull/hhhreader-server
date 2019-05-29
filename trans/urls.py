from django.urls import path

from trans import views

urlpatterns = [
    path('word/<str:word>', views.query_word, name='word_query'),
    path('paragraph/', views.query_paragraph, name='paragraph_query'),
    path('<str:user_openid>/marks/<str:word>', views.mark, name='mark'),
    path('<str:user_openid>/all/', views.query_all_marked_word, name='all_marked'),

    path('ebook/title/<str:title>', views.search_by_title, name='search_by_title'),
    path('ebook/whole/<int:idx>', views.fetch_whole_book, name='fetch_whole_book'),
    path('ebook/paragraph/<int:idx>/<int:left>/<int:right>', views.fetch_paragraph, name='fetch_paragraph'),
    path('ebook/info/<int:idx>', views.query_metadata, name='info')
]
