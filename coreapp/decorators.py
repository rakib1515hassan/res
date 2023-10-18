from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def is_subscribed(user):
    return user.customuser.is_email_verified and user.customuser.subscribed_at is not None


def subscribed_user(view_func):
    decorated_view_func = user_passes_test(
        lambda user: is_subscribed(user),
        login_url=reverse_lazy('coreapp:signin'),
        redirect_field_name=None
    )(view_func)
    return decorated_view_func