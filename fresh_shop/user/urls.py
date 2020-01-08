from django.urls import path

from user import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    # 收货地址
    path('user_site/', views.user_site, name='user_site'),
    # 全部订单
    path('user_order/', views.user_order, name='user_order'),
    # 个人中心
    path('user_center_info/', views.user_center_info, name='user_center_info'),
    # 注销
    path('logout/', views.logout, name='logout'),

]