import re

from django import forms
from django.contrib.auth.hashers import check_password

from user.models import User


class RegisterForm(forms.Form):

    user_name = forms.CharField(max_length=20,
                                min_length=5,
                                required=True,
                                error_messages={
                                    'required': '用户名必填',
                                    'max_length': '用户能超过20字符',
                                    'min_length': '用户能少于5字符'
                                })
    pwd = forms.CharField(required=True,
                          error_messages={
                              'required': '密码必填',
                              'max_length': '用户能超过20字符',
                              'min_length': '用户能少于5字符'
                          })
    email = forms.CharField(max_length=20,
                            min_length=8,
                            required=True,
                            error_messages={
                                'required': '邮箱必填'
                                            })
    cpwd = forms.CharField(max_length=20,
                           min_length=5,
                           required=True,
                           error_messages={
                                'required': '密码必填',
                                'max_length': '用户能超过20字符',
                                'min_length': '用户能少于5字符'
                           })
    allow = forms.BooleanField(required=True,
                               error_messages={
                                   'required': '必须同意协议'
                               })

    def clean_uaer_name(self):
        # 校验用户名是否被注册
        username = self.cleaned_data['user_name']
        user = User.objects.filter(username=username).first()
        if user:
            raise forms.ValidationError('该账号已注册')
        return self.cleaned_data['user_name']

    def clean(self):
        # 校验密码是否一致
        pwd = self.cleaned_data.get('pwd')
        cpwd = self.cleaned_data.get('cpwd')
        if pwd != cpwd:
            raise forms.ValidationError({'cpwd': '两次密码不一致!'})
        return self.cleaned_data

    def clean_email(self):
        # 校验邮箱格式
        email_reg = '^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$'
        email = self.cleaned_data['email']
        if not re.match(email_reg, email):
            raise forms.ValidationError('邮箱格式错误')
        return self.cleaned_data['email']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=10, required=True,
                               min_length=2,
                               error_messages={
                                   'required': '用户名必填',
                                   'max_length': '用户名最长10字符',
                                   'min_length': '用户名最少两个字符'
                               })
    pwd = forms.CharField(max_length=20, required=True,
                          min_length=6,
                          error_messages={
                              'required': '密码必填',
                              'max_length': '密码最长20个字符',
                              'min_length': '密码最短6个字符',
                          })

    def clean(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).first()
        if not user:
            raise forms.ValidationError({'username': '该用户不存在'})
        password = self.cleaned_data['pwd']
        if not check_password(password, user.password):
            raise forms.ValidationError({'pwd': '密码错误'})
        return self.cleaned_data


class AddressForm(forms.Form):
    username = forms.CharField(max_length=5, required=True,
                               error_messages={
                                   'required': '收件人必填',
                                   'max_length': '姓名不能超过5位'
                               })
    address = forms.CharField(required=True,
                              error_messages={
                                   'required': '收货地址必填',
                               })
    postcode = forms.CharField(required=True,
                               error_messages={
                                   'required': '邮编必填',
                               })
    mobile = forms.CharField(required=True,
                             error_messages={
                                   'required': '手机号必填',
                               })
