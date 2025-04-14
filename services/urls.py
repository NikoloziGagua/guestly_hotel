from django.urls import path
from . import views

urlpatterns = [
    # Existing service URLs
    path('menu/', views.food_menu, name='food_menu'),
    path('order/<int:room_number>/', views.place_food_order, name='place_food_order'),
    path('general/<int:room_number>/', views.create_general_service_request, name='create_general_service_request'),
    
    path('order/update/<int:order_id>/<str:new_status>/', views.update_food_order_status, name='update_food_order_status'),
    
    # New URLs for general service requests handled by room service:
    path('room_service/requests/', views.room_service_requests_dashboard, name='room_service_requests_dashboard'),
    path('request/update/<int:request_id>/<str:new_status>/', views.update_service_request_status, name='update_service_request_status'),
# services/urls.py
   path(
        'housekeeping/request/complete/<int:request_id>/',
        views.housekeeping_complete_service_request,
        name='housekeeping_complete_service_request_ajax'
    ),    path('request/cancel/<int:request_id>/', views.cancel_service_request, name='cancel_service_request'),
    path('room_service/request/complete/<int:request_id>/', views.complete_service_request_ajax, name='complete_service_request_ajax'),
        path('request/pending/', views.pending_service_requests, name='pending_service_requests'),
    path('dashboard/housekeeping/mark_cleaned/<int:room_id>/', views.mark_room_cleaned, name='mark_room_cleaned'),

    # Food menu management URLs for managers
    path('manager/food_menu/', views.manage_food_menu, name='manage_food_menu'),
    path('manager/food_menu/add/', views.add_food_item, name='add_food_item'),
    path('manager/food_menu/edit/<int:food_item_id>/', views.edit_food_item, name='edit_food_item'),
    path('manager/food_menu/delete/<int:food_item_id>/', views.delete_food_item, name='delete_food_item'),

    # Service request management URLs for managers
    path('manager/room-service/', views.room_service_overview, name='room_service_overview'),

    # Manager dashboard for service requests
    path('manager/service-requests/', views.view_all_service_requests, name='view_all_service_requests'),

]
