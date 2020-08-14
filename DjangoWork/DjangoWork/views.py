from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from .forms import UserLoginForm

#@login_required(login_url='/')
def login_page(request):
    if request.user.is_authenticated:
        return redirect('projects/')
    else:
        next = request.GET.get('next')
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            if next:
                return redirect(next)
            return redirect('projects/')

        context = {
            'form': form
        }
        return render(request, 'login.html', context)

def logout_view(request):
    logout(request)
    return redirect('/')

def view_404(request):
    return render(request, 'page_404.html')