from django.http import HttpResponseForbidden
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrappper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        else:
            return view_func(request, *args, **kwargs)

    return wrappper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You are not allowed to view this page")

        return wrapper_func

    return decorator


def admin_only(view_func):
    def wrapper_funcion(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == "customer":
            return redirect("userpage")
        if group == "admin":
            return view_func(request, *args, **kwargs)

    return wrapper_funcion
