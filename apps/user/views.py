from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserCreateForm, EmailLoginForm


# Create your views here.
# サインアップ
def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('user:login') # articleのindexに行くように修正必要？
    else:
        form = UserCreateForm()

    return render(request, 'user/signup.html', {'form': form})

# ログイン
def login_view(request):
    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect("article:index")
            else:
                return render(request, "user/login.html", {"error": "メールアドレスまたはパスワードが間違っています。"})
    else:
        form = EmailLoginForm()
    return render(request, "user/login.html", {"form": form})

# ログアウト
def logout_view(request):
    logout(request)
    return redirect("user:login")