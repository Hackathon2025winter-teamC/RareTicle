# レスポンスを返す

from django.shortcuts import render
from django.views import View


class IndexView(View):
    def get(self, request):
        return render(request, "diary/index.html")


index = IndexView.as_view()  # 関数に変換
