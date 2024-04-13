from django.shortcuts import render, redirect

from .forms import *


def portfolio(request):
    return render(request, 'portfolio/base.html')


def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = Profile(user=user, **profile_form.cleaned_data)
            profile.save()
            return redirect('home')
    else:
        user_form = UserForm()
        profile_form = ProfileForm()

    fields = list(user_form)[:3] + list(profile_form) + list(user_form)[3:]
    return render(request, 'portfolio/Registration.html', {'form_fields': fields})
