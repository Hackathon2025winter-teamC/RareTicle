import requests
from django.shortcuts import render
from django.core.cache import cache
from django.http import HttpResponseNotFound
from django.conf import settings
from .forms import SearchForm
import logging

logger = logging.getLogger(__name__)

#Qiita API から記事を取得
def get_qiita_articles(query):
    url = settings.QIITA_API_URL  
    headers = {"Authorization": f"Bearer {settings.QIITA_ACCESS_TOKEN}"}
    params = {
        "page": 1,
        "per_page": 10,
        "query": query
    }
    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Qiita API エラー: {e}")
        return []

#記事一覧ページ
def article_list(request):
    form = SearchForm(request.GET)
    query = request.GET.get("query", "").strip()

    cache_key = f"articles_{query.lower()}"
    articles = cache.get(cache_key)

    if not articles:
        logger.info(f"キャッシュが見つからないため、新規取得: {query}")
        qiita_articles = get_qiita_articles(query)

        articles = [
            {"id": article["id"], "title": article["title"], "url": article["url"]}
            for article in qiita_articles
        ]
        cache.set(cache_key, articles, timeout=3600)

    return render(request, "index.html", {"articles": articles, "form": form})

#記事詳細ページ
def article_detail(request, article_id):
    """
    記事の詳細情報を取得:
    1. 検索クエリに基づいたキャッシュから検索
    2. キャッシュにない場合は API から取得
    """
    query = request.GET.get("query", "").strip()
    cache_key = f"articles_{query.lower()}" if query else None

    articles = cache.get(cache_key, []) if cache_key else []
    article = next((a for a in articles if str(a["id"]) == str(article_id)), None)

    #キャッシュにない場合 API から取得
    if not article and query:
        logger.info(f"記事 {article_id} がキャッシュにないため API から取得: {query}")
        api_articles = get_qiita_articles(query)
        article = next((a for a in api_articles if str(a["id"]) == str(article_id)), None)

        if article:
            cache.set(f"articles_{query.lower()}", api_articles, timeout=3600)

    if not article:
        return HttpResponseNotFound("記事が見つかりませんでした")

    return render(request, "middle.html", {"article": article})
