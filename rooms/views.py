from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Room, Booking
from .forms import BookingForm, RoomForm
from django.utils import timezone
from django.contrib import messages 
from users.decorators import manager_required
from payments.models import SalaryRate, SalaryRecord  # Ensure these are imported
from users.decorators import receptionist_required, manager_required, housekeeping_required
# ------------------------------------------------------------------------------
# View: room_list
# This view remains simple: it queries for available rooms and passes them
# to the template. No business logic is needed here.
# ------------------------------------------------------------------------------
@login_required
def room_list(request):
    # Query all rooms that are available
    rooms = Room.objects.filter(status='available')
    context = {'rooms': rooms}
    return render(request, 'rooms/room_list.html', context)

# ------------------------------------------------------------------------------
# View: create_booking
# This view handles booking creation. Instead of doing price calculations and
# status updates here, it calls a model method (process_booking) that encapsulates
# that logic.
# ------------------------------------------------------------------------------#
#login_required
def create_booking(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Create a booking instance without saving it immediately
            booking = form.save(commit=False)
            booking.guest = request.user         # Associate booking with current user
            booking.room = room                  # Link the booking to the selected room
            booking.status = 'reserved'          # Set initial status
            booking.process_booking()            # Delegate business logic to the model method

            messages.success(request, "Booking created successfully.")
            return redirect('guest_dashboard')
    else:
        form = BookingForm()

    context = {'form': form, 'room': room}
    return render(request, 'rooms/create_booking.html', context)

# ------------------------------------------------------------------------------
# View: cancel_booking
# Cancelling a booking should simply update the booking and room statuses.
# If you have a model method for cancellation, that would be even better.
# Here, we check the state and then update the status.
# ------------------------------------------------------------------------------
@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, guest=request.user)

    if booking.status == 'reserved':
        # Directly update booking status to 'cancelled'
        booking.status = 'cancelled'
        booking.save()
        # Update room status; ideally, you could call a model method on room too
        room = booking.room
        room.status = 'available'
        room.save()
        messages.success(request, "Your booking has been cancelled.")
    else:
        messages.error(request, "This booking cannot be cancelled at this stage.")
    
    return redirect('guest_dashboard')

# ------------------------------------------------------------------------------
# View: receptionist_dashboard
# This view collects the current bookings (reserved and checked-in) and passes
# them to the template. No changes needed as business logic is minimal.
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
# View: check_in_booking
# Instead of manually setting statuses in the view, call a model method on booking.
# ------------------------------------------------------------------------------

@login_required
@receptionist_required

def check_in_booking(request, booking_id):
    print("🔵 Check-In View Triggered")
    booking = get_object_or_404(Booking, id=booking_id)
    print("🔎 Booking status:", booking.status)
    
    if booking.status == 'reserved':
        booking.status = 'checked_in'
        booking.save()
        booking.room.status = 'occupied'
        booking.room.save()
        messages.success(request, "Check-in successful.")
        print("✅ Check-in completed successfully.")

        receptionist_rate = SalaryRate.objects.filter(role='receptionist').first()
        if receptionist_rate:
            SalaryRecord.objects.create(
                role='receptionist',
                amount=receptionist_rate.rate,
                description=f"Checked in booking #{booking.id}"
            )
            print("💰 Receptionist salary recorded successfully.")
        else:
            print("❌ SalaryRate not found for receptionist!")
    else:
        messages.error(request, "Cannot check-in: Incorrect booking status.")
        print("🚫 Check-in failed due to incorrect booking status:", booking.status)

    return redirect('receptionist_dashboard')


@login_required
@receptionist_required

def check_out_booking(request, booking_id):
    print("🔵 Check-Out View Triggered")
    booking = get_object_or_404(Booking, id=booking_id)
    print("🔎 Booking status:", booking.status)
    
    if booking.status == 'checked_in':
        booking.status = 'checked_out'
        booking.save()
        booking.room.status = 'needs_cleaning'
        booking.room.dirty_since = timezone.now()
        booking.room.save()
        messages.success(request, "Check-out successful.")
        print("✅ Check-out completed successfully.")

        receptionist_rate = SalaryRate.objects.filter(role='receptionist').first()
        if receptionist_rate:
            SalaryRecord.objects.create(
                role='receptionist',
                amount=receptionist_rate.rate,
                description=f"Checked out booking #{booking.id}"
            )
            print("💰 Receptionist salary recorded successfully.")
        else:
            print("❌ SalaryRate not found for receptionist!")
    else:
        messages.error(request, "Cannot check-out: Incorrect booking status.")
        print("🚫 Check-out failed due to incorrect booking status:", booking.status)

    return redirect('receptionist_dashboard')

# ------------------------------------------------------------------------------
# View: mark_room_cleaned
# Instead of updating the room directly in the view, call the mark_as_cleaned method.
# ------------------------------------------------------------------------------
@login_required
@housekeeping_required
def mark_room_cleaned(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    
    if room.status == 'needs_cleaning':
        room.mark_as_cleaned()  # Use model method to update room status
        messages.success(request, f"Room {room.room_number} marked as clean and available.")
        
        # If the user is housekeeping, log the salary record for cleaning
        if request.user.role == 'housekeeping':
            try:
                rate_obj = SalaryRate.objects.get(role='housekeeping')
                SalaryRecord.objects.create(
                    role='housekeeping',
                    amount=rate_obj.rate,
                    description=f"Cleaned room {room.room_number}"
                )
            except SalaryRate.DoesNotExist:
                messages.warning(request, "No salary rate set for housekeeping. Please contact admin.")
    else:
        messages.error(request, f"Room {room.room_number} is not marked as needing cleaning.")
    
    return redirect('housekeeping_dashboard')

# ------------------------------------------------------------------------------
# Manager-specific views below: they are straightforward, handling forms and
# simple CRUD operations on Room objects.
# ------------------------------------------------------------------------------
@login_required#
@manager_required
def room_management_home(request):
    rooms = Room.objects.all().order_by('room_number')
    context = {'rooms': rooms}
    return render(request, 'rooms/room_management_home.html', context)

@login_required
@manager_required
def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Room added successfully.")
            return redirect('room_management_home')
        else:
            messages.error(request, "Error adding room. Please check the form.")
    else:
        form = RoomForm()
    return render(request, 'rooms/add_room.html', {'form': form})

@login_required
@manager_required
def edit_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, "Room updated successfully.")
            return redirect('room_management_home')
        else:
            messages.error(request, "Error updating room. Please check the form.")
    else:
        form = RoomForm(instance=room)
    return render(request, 'rooms/edit_room.html', {'form': form, 'room': room})

@login_required
@manager_required
def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    room.delete()
    messages.success(request, "Room deleted successfully.")
    return redirect('room_management_home')
