from django.urls import path
from .views import news_feed, fetch_and_store_view, home_redirect

urlpatterns = [
    path('', home_redirect, name='home_redirect'),  
    path('news/', news_feed, name='news_feed'),
    path('fetch-news/', fetch_and_store_view, name='fetch_and_store_view'),  
]
