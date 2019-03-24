import csv
import os
from datetime import datetime
import django
path =  os.getcwd()
os.chdir(path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ordersite.settings")
django.setup()
from orderapp.models import Order, OrderItem

orders = Order.objects.all()
order_items = OrderItem.objects.all()
orders.delete()
order_items.delete()

