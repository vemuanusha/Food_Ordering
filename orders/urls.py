from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('history/', views.order_history, name='history'),
    path('place/', views.place_order, name='place_order'),
    path('pay/<int:order_id>/', views.simulate_payment, name='simulate_payment'), 
]
