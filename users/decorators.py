from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse

def role_required(required_role):
    """
    Generic role requirement decorator that checks:
    1. If dev mode is enabled (bypasses restrictions)
    2. If user is authenticated
    3. If user has the required role
    
    Args:
        required_role (str): The role name required to access the view
        
    Returns:
        function: Decorated view function that enforces role-based access
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.session.get('dev_mode', False):
                return view_func(request, *args, **kwargs)

            if not request.user.is_authenticated:
                messages.error(request, "You must be logged in.")
                return redirect(reverse('login') + '?next=' + request.path)

            role_check_method = getattr(request.user, f'is_{required_role}', None)
            if not role_check_method:
                return HttpResponse(f"""
                    <script>
                        alert('Error: Role check method not found');
                        window.location.href = '{reverse('guest_dashboard')}';
                    </script>
                """)

            if not role_check_method():
                return HttpResponse(f"""
                    <script>
                        alert('Access Denied: You need {required_role} privileges');
                        window.location.href = '{reverse('guest_dashboard')}';
                    </script>
                """)

            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator

# Role-specific decorators
def receptionist_required(view_func):
    """Restrict access to receptionists only"""
    return role_required('receptionist')(view_func)

def manager_required(view_func):
    """Restrict access to managers only"""
    return role_required('manager')(view_func)

def housekeeping_required(view_func):
    """Restrict access to housekeeping staff only"""
    return role_required('housekeeping')(view_func)

def room_service_required(view_func):
    """Restrict access to room service staff only"""
    return role_required('room_service')(view_func)

def guest_required(view_func):
    """Restrict access to guests only"""
    return role_required('guest')(view_func)