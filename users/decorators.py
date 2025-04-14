from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse

def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Check developer mode from session first
            if request.session.get('dev_mode', False):
                return view_func(request, *args, **kwargs)

            # Authentication check
            if not request.user.is_authenticated:
                messages.error(request, "You must be logged in.")
                return redirect(reverse('login') + '?next=' + request.path)

            # Role check
            role_check_method = getattr(request.user, f'is_{required_role}', None)
            if not role_check_method:
                # Return response with JavaScript alert
                return HttpResponse(f"""
                    <script>
                        alert('Error: Role check method not found');
                        window.location.href = '{reverse('guest_dashboard')}';
                    </script>
                """)

            if not role_check_method():
                # Return response with JavaScript alert
                return HttpResponse(f"""
                    <script>
                        alert('Access Denied: You need {required_role} privileges');
                        window.location.href = '{reverse('guest_dashboard')}';
                    </script>
                """)

            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator

# Specific role decorators remain the same
def receptionist_required(view_func):
    return role_required('receptionist')(view_func)

def manager_required(view_func):
    return role_required('manager')(view_func)

def housekeeping_required(view_func):
    return role_required('housekeeping')(view_func)

def room_service_required(view_func):
    return role_required('room_service')(view_func)

def guest_required(view_func):
    return role_required('guest')(view_func)