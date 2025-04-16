# Import necessary modules from Django and our apps
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import Sum, Count, ExpressionWrapper, F, DecimalField  # Import Sum, Count, ExpressionWrapper, F, and DecimalField for aggregation
from payments.models import SalaryRecord, SalaryRate    
from decimal import Decimal
import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserRegisterForm
from django.utils import timezone
from users.decorators import (
    room_service_required, 
    manager_required, 
    housekeeping_required, 
    receptionist_required
)

from .forms import CustomUserCreationForm, AssignRoleForm
from users.models import CustomUser

from rooms.models import Room, Booking
from services.models import ServiceRequest, FoodOrder


def register(request):
    """
    Handle user registration using CustomUserRegisterForm.
    Sets default role as 'guest' for new registrations.
    """
    if request.method == 'POST':
        form = CustomUserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # This will automatically set role='guest'
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')
    else:
        form = CustomUserRegisterForm()
    
    return render(request, 'users/register.html', {'form': form})


@login_required
def role_based_redirect(request):
    """
    Redirect users to their appropriate dashboard based on their role.
    Uses the get_dashboard_url method from the CustomUser model.
    """
    return redirect(request.user.get_dashboard_url())



@login_required
def guest_dashboard(request):
    """
    Display guest dashboard with:
    - Active bookings
    - Available rooms (cached)
    - Food orders
    - Service requests
    - Room cost calculations
    Uses caching for available rooms to improve performance.
    """
    user = request.user
    active_booking = Booking.objects.filter(guest=user, status='checked_in').first()

    available_rooms = None
    if not active_booking:
        available_rooms = cache.get('available_rooms')
        if available_rooms is None:
            available_rooms = Room.objects.filter(status='available')
            cache.set('available_rooms', available_rooms, 120)
    
    food_orders = FoodOrder.objects.filter(guest=user)
    service_requests = ServiceRequest.objects.filter(guest=user)
    
    room_cost = 0
    if active_booking:
        nights = (active_booking.check_out_date - active_booking.check_in_date).days
        room_cost = nights * active_booking.room.price_per_night

    context = {
        'welcome_message': f"Welcome to your Dashboard, {user.username}!",
        'active_booking': active_booking,
        'available_rooms': available_rooms,
        'food_orders': food_orders,
        'service_requests': service_requests,
        'room_cost': room_cost,
    }
    return render(request, "users/guest_dashboard.html", context)




@login_required
def booking_detail(request, booking_id):
    """
    Show detailed information for a specific booking:
    - Room costs
    - Food orders and costs
    - Service requests and costs
    - Total cost calculation
    Ensures users can only view their own bookings.
    """
    booking = get_object_or_404(Booking, id=booking_id, guest=request.user)

    nights = (booking.check_out_date - booking.check_in_date).days
    room_cost = nights * booking.room.price_per_night

    food_orders = FoodOrder.objects.filter(guest=request.user, room=booking.room)
    service_requests = ServiceRequest.objects.filter(guest=request.user, room=booking.room)

    food_cost = sum(order.total_price for order in food_orders)
    service_cost = sum(req.cost for req in service_requests)
    total_cost = room_cost + food_cost + service_cost

    context = {
        'booking': booking,
        'room_cost': room_cost,
        'food_cost': food_cost,
        'service_cost': service_cost,
        'total_cost': total_cost,
        'food_orders': food_orders,
        'service_requests': service_requests,
    }
    return render(request, "users/booking_detail.html", context)


@login_required
@receptionist_required
def receptionist_dashboard(request):
    """
    Display receptionist dashboard showing:
    - Current bookings (reserved and checked-in)
    Restricted to users with receptionist role.
    """
    current_bookings = Booking.objects.filter(status__in=['reserved', 'checked_in'])
    context = {
        'welcome_message': f"Receptionist Dashboard: {request.user.username}",
        'current_bookings': current_bookings,
    }
    return render(request, "users/receptionist_dashboard.html", context)



@login_required
@housekeeping_required
def housekeeping_dashboard(request):
    """
    Display housekeeping dashboard with:
    - Rooms needing cleaning (ordered by room number)
    - Pending cleaning requests
    - In-progress cleaning tasks
    Restricted to users with housekeeping role.
    """
    # Get rooms needing cleaning
    rooms_needing_cleaning = Room.objects.filter(status='needs_cleaning').order_by('room_number')
    
    # Get cleaning requests
    cleaning_requests = ServiceRequest.objects.filter(
        request_type='cleaning',
        status__in=['pending', 'in_progress']
    ).select_related('room').order_by('created_at')
    
    context = {
        'rooms_needing_cleaning': rooms_needing_cleaning,
        'cleaning_requests': cleaning_requests,
    }
    return render(request, 'users/housekeeping_dashboard.html', context)
@login_required
def room_service_dashboard(request):
    """
    Display room service dashboard showing:
    - Active food orders (excluding delivered/canceled)
    - Pending service requests (excluding cleaning)
    - Current time for order tracking
    Uses select_related for optimized database queries.
    """
    # Get pending food orders (excluding completed/canceled)
    food_orders = FoodOrder.objects.exclude(
        status__in=['delivered', 'canceled']
    ).select_related('guest', 'room').order_by('ordered_at')
    
    # Get service requests (excluding cleaning and completed)
    service_requests = ServiceRequest.objects.exclude(
        request_type='cleaning'
    ).exclude(
        status='completed'
    ).select_related('guest', 'room').order_by('created_at')
    
    context = {
        'welcome_message': f"Welcome, {request.user.get_full_name() or request.user.username}",
        'orders': food_orders,
        'service_requests': service_requests,
        'current_time': timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    return render(request, 'users/room_service_dashboard.html', context)





@login_required
@manager_required
def manager_control_panel(request):
    """
    Comprehensive management interface showing:
    - All rooms (cached)
    - All users (cached)
    - All bookings
    - All food orders
    - All service requests
    Uses caching for stable data to improve performance.
    """
    rooms = cache.get('stable_rooms')
    if rooms is None:
        rooms = Room.objects.all()
        cache.set('stable_rooms', rooms, 300)  

    users = cache.get('stable_users')
    if users is None:
        users = CustomUser.objects.all()
        cache.set('stable_users', users, 300)  

    bookings = Booking.objects.all().order_by('-check_in_date')
    food_orders = FoodOrder.objects.all()  
    service_requests = ServiceRequest.objects.all()  

    context = {
        "welcome_message": f"Manager Control Panel: {request.user.username}",
        "rooms": rooms,
        "bookings": bookings,
        "users": users,
        "food_orders": food_orders,
        "service_requests": service_requests,
    }
    return render(request, "users/manager_control_panel.html", context)
@login_required
@manager_required
def manager_reports(request):
    """
    Generate financial and operational reports including:
    - Staff salary data and task completion
    - Revenue from rooms, food, and services
    - Profit calculations (75% of room revenue)
    - Maintenance cost allocation (25% of room revenue)
    Uses complex database aggregations for calculations.
    """
    
    salary_data = SalaryRecord.objects.values('role').annotate(
        total_tasks=Count('id'),
        total_amount=Sum('amount')
    )

    room_revenue = Booking.objects.aggregate(total=Sum('total_price'))['total'] or Decimal('0.00')

    computed_food_orders = FoodOrder.objects.annotate(
        computed_total=Sum(
            ExpressionWrapper(
                F('foodorderitem__quantity') * F('foodorderitem__food_item__price'),
                output_field=DecimalField()
            )
        )
    )
    food_revenue = computed_food_orders.aggregate(total=Sum('computed_total'))['total'] or 0

    service_revenue = ServiceRequest.objects.aggregate(total=Sum('cost'))['total'] or 0

    profit = room_revenue * Decimal('0.75')
    maintenance_cost = room_revenue * Decimal('0.25')

    context = {
        'salary_data': salary_data,
        'room_revenue': room_revenue,
        'food_revenue': food_revenue,
        'service_revenue': service_revenue,
        'profit': profit,
        'maintenance_cost': maintenance_cost,
        'welcome_message': f"Manager Analytics & Reports - {request.user.username}",
    }
    return render(request, 'users/manager_reports.html', context)

@login_required
@manager_required
def view_all_bookings(request):
    """
    Display all bookings in the system:
    - Ordered by check-in date
    - Includes related guest and room data
    Uses select_related for optimized queries.
    """
    bookings = Booking.objects.select_related('guest', 'room').order_by('-check_in_date')
    context = {
        'bookings': bookings,
        'welcome_message': f"Viewing all bookings - {request.user.username}",
    }
    return render(request, 'users/view_all_bookings.html', context)


def billing_dashboard(request):
    """Placeholder for future billing dashboard implementation."""
    return HttpResponse("Billing dashboard will go here.")


@login_required
@manager_required
def view_all_users(request):
    """
    Display all users in the system ordered by join date.
    Restricted to manager role.
    """
    users = CustomUser.objects.all().order_by('-date_joined')
    return render(request, 'users/view_all_users.html', {'users': users})


@login_required
@manager_required
def delete_user(request, user_id):
    """
    Handle user deletion with confirmation step.
    Restricted to manager role.
    """
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully!')
        return redirect('view_all_users')
    return render(request, 'users/delete_user.html', {'user': user})

@login_required
@manager_required
def assign_user_role(request):
    """
    Allow managers to assign different roles to users.
    Handles form validation and role updates.
    """
    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            role = form.cleaned_data['role']
            user.role = role  # Update the user's role
            user.save()       # Persist the change
            messages.success(request, f"{user.username} is now a {role}.")
            return redirect('manager_control_panel')
    else:
        form = AssignRoleForm()

    return render(request, 'users/assign_user_role.html', {'form': form})

@require_POST
def toggle_dev_mode(request):
    """
    Toggle development mode in session.
    Used for debugging and testing features.
    """
    if 'dev_mode' not in request.session:
        request.session['dev_mode'] = False
    request.session['dev_mode'] = not request.session['dev_mode']
    request.session.modified = True
    return JsonResponse({'status': 'ok', 'dev_mode': request.session['dev_mode']})

@login_required
def add_user(request):
    """
    Handle creation of new users with specified roles.
    Uses CustomUserCreationForm for validation.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data['role']  
            user.save()
            messages.success(request, f'User {user.username} created successfully with {user.get_role_display()} role!')
            return redirect('view_all_users')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/add_user.html', {'form': form})

@login_required
@manager_required
def reset_user_password(request, user_id):
    """
    Initiate password reset for specified user.
    Sends reset instructions via email.
    """
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        messages.success(request, f'Password reset instructions sent to {user.email}')
        return redirect('edit_user', user_id=user.id)
    return redirect('edit_user', user_id=user.id)
@login_required
def view_all_users(request):
    """
    Display all users in the system ordered by join date.
    Restricted to manager role.
    """
    users = CustomUser.objects.all().order_by('-date_joined')
    return render(request, 'users/view_all_users.html', {'users': users})
@login_required
