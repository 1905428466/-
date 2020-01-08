from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from goods.models import Goods, GoodsCategory
from user.models import User
from django.http import HttpResponseRedirect, JsonResponse


def index(request):
    if request.method == 'GET':
        # 如果访问首页，返回渲染的首页index.html页面
        # return render(request, 'index.html')
        categorys = GoodsCategory.objects.all()
        # goods = Goods.objects.all()
        result = []
        for category in categorys:
            goods = category.goods_set.all()[:4]
            data = [category, goods]
            result.append(data)
        category_type = GoodsCategory.CATEGORY_TYPE
        sess = request.session.get('user_id')
        user = User.objects.filter(pk=sess).first()

        return render(request, 'index.html', {'result': result,
                                              'category_type': category_type,
                                              'user': user})


def detail(request, id):
    if request.method == 'GET':
        # 返回详情页面解析商品信息

        goods = Goods.objects.filter(pk=id).first()
        if request.session.get('id'):
            num = request.session['id']
            num.append(id)
            request.session['id'] = num
        else:
            request.session['id'] = [id]

        return render(request, 'detail.html', {'goods': goods})


def search(request):
    if request.method == 'GET':
        content = request.GET.get('content')
        error_msg = ''
        if not content:
            error_msg = '请输入有效关键字'
            return render(request, 'list.html', {'error_msg': error_msg})
        good = Goods.objects.filter(name__icontains=content)

        return render(request, 'list.html', {'good': good, 'error_msg': error_msg})


def goods_list(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        goods = Goods.objects.filter(category_id=id)
        return render(request, 'list.html', {'goods': goods})