from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
from cart.models import ShoppingCart
from fresh_shop.settings import ORDER_NUMBER
from goods.models import Goods
from order.models import OrderInfo
from user.forms import RegisterForm, LoginForm, AddressForm
from user.models import User, UserAddress


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')

    if request.method == 'POST':
        # 使用表单from做校验
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 账号不存在于数据库，密码和第二次密码一致，邮箱格式正确
            username = form.cleaned_data['user_name']
            password = make_password(form.cleaned_data['pwd'])
            email = form.cleaned_data['email']
            User.objects.create(username=username, password=password,
                                email=email)
            return HttpResponseRedirect(reverse('user:login'))
        else:
            # 获取表单验证不通过的信息
            errors = form.errors
            return render(request, 'register.html', {'errors': errors})


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username).first()
            request.session['user_id'] = user.id
            return HttpResponseRedirect(reverse('goods:index'))
        else:
            errors = form.errors
            return render(request, 'login.html', {'errors': errors})


def user_site(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        user_address = UserAddress.objects.filter(user_id=user_id)
        active = 'site'
        return render(request, 'user_center_site.html', {'user_address': user_address,
                                                         'active': active})

    if request.method == 'POST':
        form = AddressForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            address = form.cleaned_data['address']
            postcode = form.cleaned_data['postcode']
            mobile = form.cleaned_data['mobile']
            user_id = request.session.get('user_id')
            UserAddress.objects.create(user_id=user_id,
                                       address=address,
                                       signer_name=username,
                                       signer_mobile=mobile,
                                       signer_postcode=postcode)
            return HttpResponseRedirect(reverse('user:user_site'))
        else:
            errors = form.errors
            return render(request, 'user_center_site.html', {'errors': errors})


def user_order(request):
    if request.method == 'GET':
        # 获取登录系统用户的id值
        user_id = request.session.get('user_id')

        orders = OrderInfo.objects.filter(user_id=user_id)
        status = OrderInfo.ORDER_STATUS

        page = int(request.GET.get('page', 1))
        pg = Paginator(orders, ORDER_NUMBER)
        orders = pg.page(page)
        active = 'order'
        return render(request, 'user_center_order.html', {'active': active,

                                                          'orders': orders,
                                                          'status': status})


def user_center_info(request):
    if request.method == 'GET':
        active = 'info'
        id = request.session.get('id')
        return render(request, 'user_center_info.html', {'active': active})


def logout(request):
    if request.method == 'GET':
        # 删除session中的键值
        del request.session['user_id']
        if request.session.get('user_id'):
            request.session.flush()
        return HttpResponseRedirect(reverse('goods:index'))