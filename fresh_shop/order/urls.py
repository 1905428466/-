from django.urls import path

from order import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    # 创建订单
    path('order/', views.order, name='order'),


]
