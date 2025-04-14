from django import forms
from .models import FoodOrderItem
from .models import ServiceRequest
from .models import FoodItem


class FoodOrderItemForm(forms.ModelForm):
    """
    Form for ordering a single food item with a specified quantity.
    """
    class Meta:
        model = FoodOrderItem
        fields = ['food_item', 'quantity']

class ServiceRequestForm(forms.ModelForm):
    """
    Form for creating a general service request (non-food, e.g., extra towels, cleaning).
    """
    class Meta:
        model = ServiceRequest
        fields = ['request_type', 'description']
        

class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'description', 'price', 'image']
