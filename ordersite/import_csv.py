import csv
import os
from datetime import datetime
path =  os.getcwd()
os.chdir(path)
from orderapp.models import Order, OrderItem

with open('order.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        time = row['created_at'][:row['created_at'].index(" ")]
        datetime_object = datetime.strptime(time, '%Y/%m/%d')
        p = Order(id=int(row['order_id']), customer_id=int(row['customer_id']), shipping=int(row['shipping']),created_at=datetime_object)
        p.save()
with open('order_item.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        order = Order.objects.get(id=int(row['order_id']))
        p = OrderItem(order_id= order, product_name=row['product_name'], qty=int(row['qty']))
        p.save()