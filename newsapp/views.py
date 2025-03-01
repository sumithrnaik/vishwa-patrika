from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Article, Source
from django.utils.dateparse import parse_datetime
import requests

api_key = "fa51272549cc4ed99c7970d0264e0eb6"
news_api_base_url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=" + api_key


def fetch_and_store_data(category=None):

    url = f"{news_api_base_url}&category={category}" if category else news_api_base_url

    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])

        for article in articles:
            source_data = article.get("source", {})  
            source, _ = Source.objects.get_or_create(
                source_id=source_data.get("id"),
                name=source_data.get("name")
            )

            Article.objects.update_or_create(
                url=article.get("url"),
                defaults={
                    "source": source,
                    "author": article.get("author"),
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "url_to_image": article.get("urlToImage"),
                    "published_at": parse_datetime(article.get("publishedAt")),
                    "content": article.get("content"),
                    "category": category
                }
            )
        
        return {"message": "News articles fetched and stored successfully"}

    return {"error": "Failed to fetch news"}


def fetch_and_store_view(request):

    result = fetch_and_store_data()
    return JsonResponse(result)


def news_feed(request):

    source_filter = request.GET.get('source', '').strip()
    category_filter = request.GET.get('category', '').strip()

    if category_filter and not Article.objects.filter(category=category_filter).exists():
        fetch_and_store_data(category=category_filter)

    articles = Article.objects.all().order_by('-published_at')

    if source_filter:
        articles = articles.filter(source__name__icontains=source_filter)

    if category_filter:
        articles = articles.filter(category=category_filter)

    return render(request, 'news_feed.html', {'articles': articles})


def home_redirect(request):
    
    fetch_and_store_data()  
    return redirect('news_feed')
