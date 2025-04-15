from venv import logger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import cache_page

from users.decorators import room_service_required, manager_required, housekeeping_required, receptionist_required
from .models import FoodItem, FoodOrder, FoodOrderItem, ServiceRequest
from .forms import FoodOrderItemForm, ServiceRequestForm, FoodItemForm
from rooms.models import Room, Booking
from payments.models import SalaryRate, SalaryRecord
#define httpresponse
from django.http import JsonResponse
from django.views.decorators.http import require_POST

@login_required
def mark_room_cleaned(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    
    if room.status == 'needs_cleaning':
        room.mark_as_cleaned()
        messages.success(request, f"Room {room.room_number} marked as clean")

        try:
            rate = SalaryRate.objects.get(role='housekeeping')
            SalaryRecord.objects.create(
                role='housekeeping',
                amount=rate.rate,
                description=f"Cleaned room {room.room_number}"
            )
        except SalaryRate.DoesNotExist:
            messages.warning(request, "Cleaning recorded but salary rate not configured")
    else:
        messages.error(request, f"Room {room.room_number} doesn't need cleaning")
    
    return redirect('housekeeping_dashboard')



# ------------------------------------------------------------------------------  
# --------------------- ROOM SERVICE TASKS -------------------------------------  
# ------------------------------------------------------------------------------

@login_required
def update_food_order_status(request, order_id, new_status):
    order = get_object_or_404(FoodOrder, id=order_id)
    
    # Handle different status updates for food orders
    if new_status == 'preparing':
        order.mark_as_preparing()  # Use model method to update status
        messages.success(request, f"Order #{order.id} updated to preparing.")
    elif new_status == 'delivered':
        order.mark_as_delivered()  # Use model method to update delivery status
        messages.success(request, f"Order #{order.id} updated to delivered.")
    else:
        messages.error(request, "Invalid status update requested.")
        return redirect('room_service_dashboard')
    
    # Create salary record for room service staff when they update orders
    if request.user.role == 'room_service':
        try:
            # Get the predefined salary rate for room service staff
            rate_obj = SalaryRate.objects.get(role='room_service')
            # Create a new salary record for this task
            SalaryRecord.objects.create(
                role='room_service',
                amount=rate_obj.rate,
                description=f"Updated food order #{order.id} to {new_status}"
            )
        except SalaryRate.DoesNotExist:
            messages.warning(request, "No salary rate set for room service. Please contact admin.")
    
    return redirect('room_service_dashboard')


@login_required
@require_POST
def housekeeping_complete_service_request(request, request_id):
    try:
        service_request = get_object_or_404(ServiceRequest, id=request_id)
        
        # Verify it's a cleaning request
        if service_request.request_type != 'cleaning':
            return JsonResponse({
                "status": "error",
                "message": "Invalid request type"
            }, status=400)

        service_request.mark_as_completed()
        service_request.save()

        # Salary recording
        try:
            rate_obj = SalaryRate.objects.get(role='housekeeping')
            SalaryRecord.objects.create(
                role='housekeeping',
                amount=rate_obj.rate,
                description=f"Completed cleaning request #{service_request.id}"
            )
        except SalaryRate.DoesNotExist:
            logger.error("Housekeeping salary rate not configured")
            return JsonResponse({
                "status": "error",
                "message": "Salary configuration error"
            }, status=500)

        return JsonResponse({
            "status": "success",
            "message": "Cleaning request completed successfully",
            "request_id": request_id
        })

    except Exception as e:
        logger.error(f"Error completing request: {str(e)}")
        return JsonResponse({
            "status": "error",
            "message": "Internal server error"
        }, status=500)                                      
def update_service_request_status(request, request_id, new_status):
    service_request = get_object_or_404(ServiceRequest, id=request_id)
    if new_status in ['in_progress', 'completed', 'cancelled']:
        if new_status == 'in_progress':
            service_request.mark_as_in_progress()
        elif new_status == 'completed':
            service_request.mark_as_completed()
        elif new_status == 'cancelled':
            service_request.mark_as_cancelled()
        messages.success(request, f"Service Request #{service_request.id} updated to {new_status}.")
        
        if request.user.role == 'room_service':
            try:
                rate_obj = SalaryRate.objects.get(role='room_service')
                SalaryRecord.objects.create(
                    role='room_service',
                    amount=rate_obj.rate,
                    description=f"Updated service request #{service_request.id} to {new_status}"
                )
            except SalaryRate.DoesNotExist:
                messages.warning(request, "No salary rate set for room service. Please contact admin.")
    else:
        messages.error(request, "Invalid status update.")
    
    return redirect('room_service_requests_dashboard')


@login_required
@require_POST  
def complete_service_request_ajax(request, request_id):
    try:
        service_request = get_object_or_404(ServiceRequest, id=request_id)
        service_request.mark_as_completed()
        
        # Debug print
        print(f"Marked request {request_id} as completed")
        
        rate_obj = SalaryRate.objects.get(role='room_service')
        SalaryRecord.objects.create(
            role='room_service',
            amount=rate_obj.rate,
            description=f"Completed service request #{service_request.id}"
        )
        
        return JsonResponse({
            "status": "success",
            "message": "Task Completed",
            "request_id": request_id
        }, status=200)
        
    except SalaryRate.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": "Salary rate not configured"
        }, status=500)
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)

@login_required
def cancel_service_request(request, request_id):
    """
    Allows a guest to cancel a pending service request.
    Only requests with status 'pending' can be canceled.
    """
    service_request = get_object_or_404(ServiceRequest, id=request_id, guest=request.user)
    
    if service_request.status != 'pending':
        messages.error(request, "You can only cancel requests that are still pending.")
    else:
        service_request.mark_as_cancelled()  # Delegate cancellation logic to the model
        messages.success(request, "Service request cancelled successfully.")
    
    return redirect('guest_dashboard')




@login_required
@cache_page(300)
def food_menu(request):
    items = FoodItem.objects.all()
    active_booking = Booking.objects.filter(guest=request.user, status='checked_in').first()
    context = {
        'food_items': items,
        'active_booking': active_booking,
    }
    return render(request, 'services/food_menu.html', context)


@login_required
def place_food_order(request, room_number):
    room = get_object_or_404(Room, room_number=room_number)
    active_booking = Booking.objects.filter(guest=request.user, room=room, status='checked_in').first()
    if not active_booking:
        messages.error(request, "You are not currently checked into this room. Food orders can only be placed when checked in.")
        return redirect('guest_dashboard')
    
    if request.method == 'POST':
        form = FoodOrderItemForm(request.POST)
        if form.is_valid():
            food_order = FoodOrder.objects.create(guest=request.user, room=room)
            food_item = form.cleaned_data['food_item']
            quantity = form.cleaned_data['quantity']
            FoodOrderItem.objects.create(food_order=food_order, food_item=food_item, quantity=quantity)
            messages.success(request, "Food order placed successfully.")
            return redirect('guest_dashboard')
        else:
            messages.error(request, "Error processing your food order. Please try again.")
    else:
        form = FoodOrderItemForm()
    
    context = {
        'form': form,
        'room': room,
    }
    return render(request, 'services/place_food_order.html', context)


@login_required
def create_general_service_request(request, room_number):
    room = get_object_or_404(Room, room_number=room_number)
    active_booking = Booking.objects.filter(guest=request.user, room=room, status='checked_in').first()
    if not active_booking:
        messages.error(request, "You are not currently checked into this room. Service requests can only be placed when checked in.")
        return redirect('guest_dashboard')
    
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.guest = request.user
            service_request.room = room
            service_request.save()
            messages.success(request, "Service request submitted successfully.")
            return redirect('guest_dashboard')
        else:
            messages.error(request, "There was an error processing your request. Please try again.")
    else:
        form = ServiceRequestForm()
    
    context = {'form': form, 'room': room}
    return render(request, 'services/create_general_service_request.html', context)


@login_required
@room_service_required
def pending_service_requests(request):
    # For room service, exclude cleaning requests (they go to housekeeping)
    pending_requests = ServiceRequest.objects.filter(status='pending').exclude(request_type='cleaning')
    context = {'pending_requests': pending_requests}
    return render(request, 'services/pending_service_requests.html', context)




@login_required
@room_service_required
def room_service_requests_dashboard(request):
    requests_qs = ServiceRequest.objects.filter(status__in=['pending', 'in_progress']).exclude(request_type='cleaning')
    context = {
        'welcome_message': f"Room Service Requests Dashboard: {request.user.username}",
        'service_requests': requests_qs,
    }
    return render(request, 'users/room_service_requests_dashboard.html', context)


# Manager views for Food Menu Management and Overviews remain unchanged

@login_required
@manager_required
def manage_food_menu(request):
    food_items = FoodItem.objects.all().order_by('name')
    context = {
        'food_items': food_items,
        'welcome_message': f"Food Menu Management: {request.user.username}",
    }
    return render(request, 'services/manage_food_menu.html', context)

@login_required
@manager_required
def add_food_item(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Food item added successfully.")
            return redirect('manage_food_menu')
        else:
            messages.error(request, "Error adding food item. Please correct the errors below.")
    else:
        form = FoodItemForm()
    return render(request, 'services/add_food_item.html', {'form': form})

@login_required
@manager_required
def edit_food_item(request, food_item_id):
    food_item = get_object_or_404(FoodItem, id=food_item_id)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES, instance=food_item)
        if form.is_valid():
            form.save()
            messages.success(request, "Food item updated successfully.")
            return redirect('manage_food_menu')
        else:
            messages.error(request, "Error updating food item. Please correct the errors below.")
    else:
        form = FoodItemForm(instance=food_item)
    return render(request, 'services/edit_food_item.html', {'form': form, 'food_item': food_item})

@login_required
@manager_required
def delete_food_item(request, food_item_id):
    food_item = get_object_or_404(FoodItem, id=food_item_id)
    food_item.delete()
    messages.success(request, "Food item deleted successfully.")
    return redirect('manage_food_menu')

@login_required
@manager_required
def room_service_overview(request):
    orders = FoodOrder.objects.select_related('guest', 'room').order_by('-ordered_at')
    stats = {
        'total': orders.count(),
        'pending': orders.filter(status='pending').count(),
        'preparing': orders.filter(status='preparing').count(),
        'delivered': orders.filter(status='delivered').count(),
    }
    context = {
        'orders': orders,
        'stats': stats,
        'welcome_message': f"Room Service Overview - {request.user.username}"
    }
    return render(request, 'users/room_service_overview.html', context)

@login_required
@manager_required
def view_all_service_requests(request):
    requests_list = ServiceRequest.objects.select_related('guest', 'room').order_by('-created_at')
    context = {
        'requests': requests_list,
        'welcome_message': f"All Service Requests - {request.user.username}",
    }
    return render(request, 'users/view_all_service_requests.html', context)
