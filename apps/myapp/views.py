from django.shortcuts import render
from django.views import View


class IndexView(View):
    def get(self, request):
        return render (request, 'login/login.html')
    

login = IndexView.as_view() #login/urls.pyで使用