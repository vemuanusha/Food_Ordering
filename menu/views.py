from django.shortcuts import render
from .models import MenuItem

def menu_list(request):
    items = MenuItem.objects.filter(is_available=True)
    return render(request, "menu/menu_list.html", {"items": items})
