from django.urls import path
from .views import news_feed,fetch_and_store_data

urlpatterns = [
    path('',fetch_and_store_data,name='fetch_and_store_data'),
    path('', news_feed, name='news_feed'),
]
