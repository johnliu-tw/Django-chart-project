from django.shortcuts import render
from django.template import loader
from django.http import Http404, HttpResponse
from django.db.models import Sum
from .models import Order, OrderItem
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column
from bokeh.transform import cumsum
from bokeh.embed import components
from bokeh.models import HoverTool

from math import pi
import pandas as pd

def index(request):
    order_items = OrderItem.objects.all()
    orders = Order.objects.all()

    # get shipping pie chart
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
    print(data)
    plot.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend='label', source=data)
    plot.axis.axis_label=None
    plot.axis.visible=False
    plot.grid.grid_line_color = None

    # get customer bought data
    time_list = set([time.strftime("%Y-%m-%d") for time in orders.values_list('created_at', flat=True)])
    time_list = sorted(time_list)
    orders_time_ordered = [[],[]]
    orders_time_ordered_list = []
    for time in time_list:
        order_date_count = len(orders.filter(created_at=time))
        orders_time_ordered[0].append(order_date_count)
        orders_time_ordered[1].append(time)
        orders_time_ordered_list.append({'order_date_count': order_date_count, 'time': time})
        
    plot2 = figure(plot_width=1000, plot_height=350, title="Customer Bought Cohort", x_range=orders_time_ordered[1])
    plot2.line(orders_time_ordered[1], orders_time_ordered[0])

    
    # get popular products
    popular_product_lists = OrderItem.objects.values('product_name').annotate(qty = Sum('qty')).order_by('-qty')[:3]
    popular_products = [[],[]]
    for product in popular_product_lists:
        popular_products[0].append(product['product_name'])
        popular_products[1].append(product['qty'])
    
    print(popular_products)
    plot3 = figure(plot_width=1000, plot_height=400, title="Popular Product List", x_range=popular_products[0])
    plot3.vbar(x=popular_products[0], top=popular_products[1], width=0.9, color=['firebrick','coral','wheat'])
    layouts = column(plot, plot2)

    script, div = components(layouts)
    script2, div2 = components(plot3)

    template = loader.get_template('orderapp/index.html')
    context = {
        'orders_time_ordered': orders_time_ordered,
        'popular_product_lists': popular_product_lists,
        'orders_time_ordered_list': orders_time_ordered_list,
        'script': script,
        'script2': script2,
        'div': div,
        'div2': div2

    }
    return HttpResponse(template.render(context, request))
