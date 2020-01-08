from django.urls import path

from goods import views

urlpatterns = [
        # 搜索
        path('search/', views.search, name='search'),
        path('index/', views.index, name='index'),
        path('detail/<int:id>/', views.detail, name='detail'),
        path('goods_list/', views.goods_list, name='goods_list'),

]