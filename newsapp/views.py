from django.shortcuts import render
from django.http import JsonResponse
from .models import Article,Source
from django.utils.dateparse import parse_datetime
import requests

api_key="fa51272549cc4ed99c7970d0264e0eb6"
news_api_url=f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"

def fetch_and_store_data(request, category=None):

    if category:
        news_api_url = f"https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={api_key}"
    else:
        news_api_url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"

    response = requests.get(news_api_url)
    
    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        saved_articles = []

        for article in articles:
            source_data = article.get("source", {}) 
            source, created = Source.objects.get_or_create(
                source_id=source_data.get("id"),
                name=source_data.get("name")
            )

            article_obj, _ = Article.objects.update_or_create(
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
            saved_articles.append(article_obj.title)

        return JsonResponse({
            "message": "News articles fetched and stored successfully",
            "saved_articles": saved_articles
        })
    
    return JsonResponse({"error": "Failed to fetch news"}, status=400)



def news_feed(request):

    source_filter = request.GET.get('source', '').strip()
    category_filter = request.GET.get('category', '').strip()

    articles = Article.objects.all().order_by('-published_at') 

    if source_filter:
        articles = articles.filter(source__name__icontains=source_filter)

    if category_filter:
        if not Article.objects.filter(category=category_filter).exists():
            fetch_and_store_data(request, category=category_filter)

        articles = articles.filter(category=category_filter)

    return render(request, 'news_feed.html', {'articles': articles})




