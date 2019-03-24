from django.test import TestCase
from django.urls import resolve
from . import views
from .models import Order, OrderItem
import os

class OrderAppTest(TestCase):

    def test_root_url_to_correct_view(self):
        found = resolve('/orderapp/')  
        self.assertEqual(found.func, views.index) 
    def test_chart1_url_to_correct_view(self):
        found = resolve('/orderapp/chart1')  
        self.assertEqual(found.func, views.chart1) 
    def test_chart2_url_to_correct_view(self):
        found = resolve('/orderapp/chart2')  
        self.assertEqual(found.func, views.chart2) 
    def test_chart3_url_to_correct_view(self):
        found = resolve('/orderapp/chart3')  
        self.assertEqual(found.func, views.chart3) 
    def test_root_response_correct(self):
        response = self.client.get('/orderapp/')
        self.assertEqual(response.status_code, 200)
    def test_chart1_response_correct(self):
        response = self.client.get('/orderapp/chart1')
        self.assertEqual(response.status_code, 200)
    def test_chart2_response_correct(self):
        response = self.client.get('/orderapp/chart2')
        self.assertEqual(response.status_code, 200)
    def test_chart3_response_correct(self):
        response = self.client.get('/orderapp/chart3')
        self.assertEqual(response.status_code, 200)
    def test_generate_chart1_correct(self):
        orders = Order.objects.all()
        script, div = views.generate_chart1(orders)
        self.assertEqual(type(script), type(""))
        self.assertEqual(type(div), type(""))
    def test_generate_chart2_correct(self):
        orders = Order.objects.all()
        order_items = OrderItem.objects.all()
        orders_time_ordered,orders_time_ordered_list,orders_time_bought_list,script,div = views.generate_chart2(orders, order_items)
        self.assertEqual(type(script), type(""))
        self.assertEqual(type(div), type(""))
    def test_generate_chart3_correct(self):
        order_items = OrderItem.objects.all()
        popular_product_lists, script, div = views.generate_chart3(order_items)
        self.assertEqual(type(script), type(""))
        self.assertEqual(type(div), type(""))

    
