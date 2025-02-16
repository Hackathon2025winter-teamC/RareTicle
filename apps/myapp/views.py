from django.shortcuts import render
from .models import Article
import requests
from django.http import JsonResponse

def get_qiita_posts(request):
    query = request.GET.get('query', 'React')  # クエリパラメータを取得（デフォルトは React）
    
    url = "https://qiita.com/api/v2/items"
    params = {
        "page": 1,
        "per_page": 20,
        "query": query,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # HTTP エラーチェック
        
        data = response.json()  # JSON データを取得
        
        if data:  # 記事がある場合
            first_article = data[0]  # 1つ目の記事を取得
            return JsonResponse({
                "title": first_article["title"],
                "url": first_article["url"],
            })
        else:  # 記事が見つからなかった場合
            return JsonResponse({"error": "No articles found"}, status=404)
    
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
