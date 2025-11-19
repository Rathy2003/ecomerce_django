from functools import wraps

from django.shortcuts import redirect

def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('dashboard.login')
        return view_func(request, *args, **kwargs)
    return wrapper

def check_isauth(view_fucn):
    @wraps(view_fucn)
    def wrapper(request, *args, **kwargs):
        if 'user_id' in request.session:
            return redirect('dashboard')
        return view_fucn(request, *args, **kwargs)
    return wrapper