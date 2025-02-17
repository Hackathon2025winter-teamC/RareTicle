from django.shortcuts import render, redirect
from .forms import UserCreateForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

    else:
        form = UserCreateForm()

    return render(request, 'signup.html', {'form': form})