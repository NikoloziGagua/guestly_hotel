from django import forms
from .models import GENERAL_SERVICE_CHOICES, FoodOrderItem
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        
        
    class Meta:
        model = ServiceRequest
        fields = ['request_type', 'description']
        

class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'description', 'price', 'image']
