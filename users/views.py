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

# Import custom decorators that enforce role-based access
from users.decorators import (
    room_service_required, 
    manager_required, 
    housekeeping_required, 
    receptionist_required
)

# Import our custom forms and models from the users app
from .forms import CustomUserCreationForm, AssignRoleForm
from users.models import CustomUser

# Import models from other apps for cross-functional views
from rooms.models import Room, Booking
from services.models import ServiceRequest, FoodOrder
#import

# ------------------------------------------------------------------------------
# User Registration View
# This view handles new user registration. The form ensures that every new user
# is created as a 'guest' (default role) without exposing the role field.
# ------------------------------------------------------------------------------
def register(request):

    if request.method == 'POST':
        storage = messages.get_messages(request)
        for _ in storage:
            pass 
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # The form automatically sets role='guest'
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

# ------------------------------------------------------------------------------
# Role-Based Redirect View
# Instead of manually checking the user's role here, we delegate the redirection
# logic to the CustomUser model's get_dashboard_url() helper method.
# ------------------------------------------------------------------------------
@login_required
def role_based_redirect(request):
    return redirect(request.user.get_dashboard_url())

# ------------------------------------------------------------------------------
# Guest Dashboard View
# Displays the guest dashboard including active booking details, food orders,
# service requests, and calculates room cost if the guest is checked in.
# ------------------------------------------------------------------------------

@login_required
def guest_dashboard(request):
    user = request.user
    active_booking = Booking.objects.filter(guest=user, status='checked_in').first()

    # If no active booking, get available rooms from cache (or query and cache the result)
    available_rooms = None
    if not active_booking:
        available_rooms = cache.get('available_rooms')
        if available_rooms is None:
            available_rooms = Room.objects.filter(status='available')
            # Cache the available rooms query for 120 seconds (2 minutes)
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



# ------------------------------------------------------------------------------
# Booking Detail View
# Provides detailed information about a specific booking, including room cost,
# associated food orders, service requests, and a billing summary.
# ------------------------------------------------------------------------------
@login_required
def booking_detail(request, booking_id):
    # Ensure the booking exists and belongs to the current user
    booking = get_object_or_404(Booking, id=booking_id, guest=request.user)

    # Compute room cost based on booking duration and room price.
    nights = (booking.check_out_date - booking.check_in_date).days
    room_cost = nights * booking.room.price_per_night

    # Retrieve food orders and service requests for this booking.
    food_orders = FoodOrder.objects.filter(guest=request.user, room=booking.room)
    service_requests = ServiceRequest.objects.filter(guest=request.user, room=booking.room)

    # Compute costs: sum up food order totals and service request costs.
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

# ------------------------------------------------------------------------------
# Receptionist Dashboard View
# Displays all current bookings that are either reserved or checked in,
# enabling the receptionist to process check-in and check-out actions.
# ------------------------------------------------------------------------------
@login_required
@receptionist_required
def receptionist_dashboard(request):
    current_bookings = Booking.objects.filter(status__in=['reserved', 'checked_in'])
    context = {
        'welcome_message': f"Receptionist Dashboard: {request.user.username}",
        'current_bookings': current_bookings,
    }
    return render(request, "users/receptionist_dashboard.html", context)

# ------------------------------------------------------------------------------
# Housekeeping Dashboard View
# Displays rooms that need cleaning and any pending service requests.
# ------------------------------------------------------------------------------

@login_required
@housekeeping_required
def housekeeping_dashboard(request):
    # Retrieve rooms that need cleaning (e.g., those marked as 'needs_cleaning')
    rooms_needing_cleaning = Room.objects.filter(status='needs_cleaning')
    
    # Retrieve only service requests for cleaning (i.e., request_type equals 'cleaning') that are pending
    cleaning_requests = ServiceRequest.objects.filter(status='pending', request_type='cleaning')
    
    context = {
        'rooms_needing_cleaning': rooms_needing_cleaning,
        'cleaning_requests': cleaning_requests,
        
    }
    return render(request, 'users/housekeeping_dashboard.html', context)



# ------------------------------------------------------------------------------
# Manager Control Panel View
# Aggregates data from rooms, bookings, users, food orders, and service requests
# to provide a comprehensive overview for managers.
# ------------------------------------------------------------------------------


@login_required
@manager_required
def manager_control_panel(request):
    # Cache stable data: rooms and users (rooms and user lists likely change less frequently)
    rooms = cache.get('stable_rooms')
    if rooms is None:
        rooms = Room.objects.all()
        cache.set('stable_rooms', rooms, 300)  # cache for 5 minutes

    users = cache.get('stable_users')
    if users is None:
        users = CustomUser.objects.all()
        cache.set('stable_users', users, 300)  # cache for 5 minutes

    # Fetch dynamic data directly (since they change quickly)
    bookings = Booking.objects.all().order_by('-check_in_date')
    food_orders = FoodOrder.objects.all()  # dynamic, fetched fresh
    service_requests = ServiceRequest.objects.all()  # dynamic, fetched fresh

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
    Aggregates data for the manager reports, including:
      - Salary data: Total tasks completed and total payments per role.
      - Revenue data: Total revenue from room bookings, food orders, and service requests.
      - Profit calculation: 75% of room revenue is profit, while 25% is allocated for maintenance.
    """
    # Aggregate salary data (group by role)
    salary_data = SalaryRecord.objects.values('role').annotate(
        total_tasks=Count('id'),
        total_amount=Sum('amount')
    )

    # Total room revenue (assumed that Booking.total_price is stored in the DB)
    room_revenue = Booking.objects.aggregate(total=Sum('total_price'))['total'] or Decimal('0.00')

    # Compute food revenue using an annotation because FoodOrder.total_price is a property.
    computed_food_orders = FoodOrder.objects.annotate(
        computed_total=Sum(
            ExpressionWrapper(
                F('foodorderitem__quantity') * F('foodorderitem__food_item__price'),
                output_field=DecimalField()
            )
        )
    )
    food_revenue = computed_food_orders.aggregate(total=Sum('computed_total'))['total'] or 0

    # Total service revenue from service requests (if cost is applied)
    service_revenue = ServiceRequest.objects.aggregate(total=Sum('cost'))['total'] or 0

    # Compute profit and maintenance cost from room revenue
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
# ------------------------------------------------------------------------------
# View All Bookings (Manager Use)
# Displays a comprehensive list of all bookings with related guest and room data.
# ------------------------------------------------------------------------------
@login_required
@manager_required
def view_all_bookings(request):
    bookings = Booking.objects.select_related('guest', 'room').order_by('-check_in_date')
    context = {
        'bookings': bookings,
        'welcome_message': f"Viewing all bookings - {request.user.username}",
    }
    return render(request, 'users/view_all_bookings.html', context)

# ------------------------------------------------------------------------------
# Billing Dashboard and Manager Reports (Placeholders)
# These are placeholders for future functionality.
# ------------------------------------------------------------------------------
def billing_dashboard(request):
    return HttpResponse("Billing dashboard will go here.")

# ------------------------------------------------------------------------------
# View All Users (Manager Use)
# Displays a list of all registered users for managerial oversight.
# ------------------------------------------------------------------------------
@login_required
@manager_required
def view_all_users(request):
    users = CustomUser.objects.all().order_by('-date_joined')
    context = {
        'users': users,
        'welcome_message': f"All Registered Users - {request.user.username}",
    }
    return render(request, 'users/view_all_users.html', context)

# ------------------------------------------------------------------------------
# Assign User Role View
# Allows managers to assign a new role to a user using a simple form.
# ------------------------------------------------------------------------------
@login_required
@manager_required
def assign_user_role(request):
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
    if 'dev_mode' not in request.session:
        request.session['dev_mode'] = False
    request.session['dev_mode'] = not request.session['dev_mode']
    request.session.modified = True
    return JsonResponse({'status': 'ok', 'dev_mode': request.session['dev_mode']})
