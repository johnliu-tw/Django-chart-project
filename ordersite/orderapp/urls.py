from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    url(r'^chart1$', views.chart1, name='chart1'),
    url(r'^chart2$', views.chart2, name='chart2'),
    url(r'^chart3$', views.chart3, name='chart3'),
]