from django.db import models
from django.conf import settings
from users.models import CustomUser
from rooms.models import Room
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


GENERAL_SERVICE_CHOICES = [
    ('towels', 'Extra Towels'),
    ('cleaning', 'Additional Cleaning'),
    ('maintenance', 'Maintenance Request'),
]

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]

FOOD_ORDER_STATUS = [
    ('pending', 'Pending'),
    ('preparing', 'Preparing'),
    ('delivered', 'Delivered'),
]


class ServiceRequest(models.Model):
    """
    Represents a service request made by a guest.
    
    Service requests can be for additional towels, cleaning, or maintenance.
    Each request tracks its status from pending through completion.
    """
    guest = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='service_requests'
    )
    room = models.ForeignKey(
        Room, 
        on_delete=models.CASCADE, 
        related_name='service_requests'
    )
    request_type = models.CharField(max_length=50, choices=GENERAL_SERVICE_CHOICES)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    cost = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.get_request_type_display()} for Room {self.room.room_number} by {self.guest.username}"


    def mark_as_in_progress(self):
        """Updates request status to 'in_progress' when staff begins working on it."""
        self.status = 'in_progress'
        self.save()

    def mark_as_completed(self):
        """Mark the service request as 'completed' and save the update."""
        self.status = 'completed'
        self.save()

    def mark_as_cancelled(self):
        """Mark the service request as 'cancelled' and save the update."""
        self.status = 'cancelled'
        self.save()


class FoodItem(models.Model):
    """
    Represents an item on the hotel's food menu.
    
    Includes details like name, description, price, and an optional image.
    """
    name = models.CharField(max_length=100)  
    description = models.TextField(blank=True)  
    price = models.DecimalField(max_digits=6, decimal_places=2)  
    image = models.ImageField(upload_to='food_items/', blank=True, null=True)  

    def __str__(self):
        return self.name


class FoodOrder(models.Model):
    """
    Represents a food order placed by a guest.
    
    Tracks the guest, room, order time, and current status of the order.
    """
    guest = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=FOOD_ORDER_STATUS, default='pending')

    @property
    def total_price(self):
        """
        Calculate the total price of the food order by summing the product of
        quantity and price for each FoodOrderItem associated with this order.
        """
        return sum(item.quantity * item.food_item.price for item in self.foodorderitem_set.all())

    def __str__(self):

        return f"Order #{self.id} by {self.guest.username}"


    def mark_as_preparing(self):
        """Update the order status to 'preparing' and save the change."""
        self.status = 'preparing'
        self.save()

    def mark_as_delivered(self):
        """Update the order status to 'delivered' and save the change."""
        self.status = 'delivered'
        self.save()


class FoodOrderItem(models.Model):
    food_order = models.ForeignKey(FoodOrder, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.food_item.name} for Order #{self.food_order.id}"
