from django.urls import path, re_path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.view_cart, name='view'),
    path('add/<int:item_id>/', views.add_to_cart, name='add'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove'),
    re_path(r'^qty/(?P<item_id>\d+)/(?P<delta>-?\d+)/$', views.change_quantity, name='qty'),
    path('place/', views.place_order, name='place'),
]
