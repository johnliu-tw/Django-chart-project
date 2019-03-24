from django.shortcuts import render
from django.template import loader
from django.http import Http404, HttpResponse
from django.db.models import Sum
from .models import Order, OrderItem
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column, row
from bokeh.transform import cumsum
from bokeh.embed import components
from bokeh.models import HoverTool

from math import pi
import pandas as pd

def index(request):
    order_items = OrderItem.objects.all()
    orders = Order.objects.all()

    # get shipping pie chart
    script, div = generate_chart1(orders)

    # get customer ordered data
    orders_time_ordered,orders_time_ordered_list,orders_time_bought_list,script2,div2 = generate_chart2(orders, order_items)

    # get popular products
    popular_product_lists, script3, div3 = generate_chart3(order_items)

    template = loader.get_template('orderapp/index.html')
    context = {
        'orders_time_ordered': orders_time_ordered,
        'popular_product_lists': popular_product_lists,
        'orders_time_ordered_list': orders_time_ordered_list,
        'orders_time_bought_list': orders_time_bought_list,
        'script': script,
        'script2': script2,
        'script3': script3,
        'div': div,
        'div2': div2,
        'div3': div3

    }
    return HttpResponse(template.render(context, request))

def chart1(request):
    orders = Order.objects.all()

    script, div = generate_chart1(orders)
    template = loader.get_template('orderapp/chart1.html')
    context = {
        'script': script,
        'div': div,
    }
    return HttpResponse(template.render(context, request))
def chart2(request):
    order_items = OrderItem.objects.all()
    orders = Order.objects.all()

    orders_time_ordered,orders_time_ordered_list,orders_time_bought_list,script,div = generate_chart2(orders, order_items)
    template = loader.get_template('orderapp/chart2.html')
    context = {
        'orders_time_ordered': orders_time_ordered,
        'orders_time_ordered_list': orders_time_ordered_list,
        'popular_product_lists': popular_product_lists,
        'script': script,
        'div': div,
    }

    return HttpResponse(template.render(context, request))

def chart3(request):
    order_items = OrderItem.objects.all()

    popular_product_lists, script, div = generate_chart3(order_items)
    template = loader.get_template('orderapp/chart3.html')
    context = {
        'popular_product_lists': popular_product_lists,
        'script': script,
        'div': div,
    }
    return HttpResponse(template.render(context, request))


def generate_chart1(orders):
    # get shipping pie chart
    orders = Order.objects.all()

    pie_x = {
        'shipping': len(orders.filter(shipping=80)),
        'no_shipping': len(orders.filter(shipping=0))
    }
    data = pd.Series(pie_x).reset_index(name='value').rename(columns={'index':'shipping-type'})
    data['angle'] = data['value']/data['value'].sum() * 2*pi
    data['color'] = ['firebrick','coral']
    data['label'] = [data['shipping-type'][0]+":" + str(data['value'][0]),
                     data['shipping-type'][1]+":" + str(data['value'][1])]

    plot = figure(plot_height=350, title="Shipping Rate Chart", x_range=(-0.5, 1.0))
    plot.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend='label', source=data)
    plot.axis.axis_label=None
    plot.axis.visible=False
    plot.grid.grid_line_color = None
    script, div = components(plot)

    return script, div

def generate_chart2(orders, order_items):
    time_list = set([time.strftime("%Y-%m-%d") for time in orders.values_list('created_at', flat=True)])
    time_list = sorted(time_list)
    orders_time_ordered = [[],[]]
    orders_time_ordered_list = []
    for time in time_list:
        order_date_count = len(orders.filter(created_at=time))
        orders_time_ordered[0].append(order_date_count)
        orders_time_ordered[1].append(time)
        orders_time_ordered_list.append({'order_date_count': order_date_count, 'time': time})
        
    plot = figure(plot_width=1000, plot_height=350, title="Customer Ordered Cohort", x_range=orders_time_ordered[1])
    plot.line(orders_time_ordered[1], orders_time_ordered[0])

    # get cutomer bought quantity data
    orders_time_bought = [[],[]]
    orders_time_bought_list = []
    per_order_quantity_list = order_items.values('order').annotate(qty=Sum('qty')).values('order','qty')
    for time in time_list:
        order_ids = list(Order.objects.filter(created_at=time).values_list('id', flat=True))
        per_day_order_quantity_list = [d for d in per_order_quantity_list if d['order'] in order_ids]
        orders_time_bought[1].append(time)
        orders_time_bought[0].append(0)        
        for per_day_order_quantity in per_day_order_quantity_list:
            orders_time_bought[0][-1] += per_day_order_quantity['qty']
        orders_time_bought_list.append({'orders_time_bought': orders_time_bought[0][-1], 'time': time})

    plot2 = figure(plot_width=1000, plot_height=350, title="Customer Bought Cohort", x_range=orders_time_bought[1])
    plot2.line(orders_time_bought[1], orders_time_bought[0]) 

    layouts = column(plot, plot2)
    script, div = components(layouts)
    return orders_time_ordered,orders_time_ordered_list,orders_time_bought_list,script,div

def generate_chart3(order_items):
    popular_product_lists = order_items.values('product_name').annotate(qty = Sum('qty')).order_by('-qty')[:3]
    popular_products = [[],[]]
    for product in popular_product_lists:
        popular_products[0].append(product['product_name'])
        popular_products[1].append(product['qty'])
    plot = figure(plot_width=1000, plot_height=400, title="Popular Product List", x_range=popular_products[0])
    plot.vbar(x=popular_products[0], top=popular_products[1], width=0.9, color=['firebrick','coral','wheat'])
    script, div = components(plot)

    return popular_product_lists, script, div