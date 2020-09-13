from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm


def register(request):
    # Registration blocked for now
    messages.info(request, 'Registration is blocked now:(')
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        """ if form.is_valid():
            form.save()
            messages.success(request, f'Account created! Now you can log in.')
            return redirect('login') """
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {
        'form': form
    })
