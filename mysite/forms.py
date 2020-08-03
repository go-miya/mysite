from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
# 创建Django表单类，用于登录
class LoginForm(forms.Form):
    username = forms.CharField(label="登录名", \
                               widget=forms.TextInput( \
                               attrs= {'class':'form-control', 'placeholder':'请输入用户名'})) # required默认是True
    password = forms.CharField(label="密码", widget=forms.PasswordInput(
                                    attrs={'class':'form-control', 'placeholder':'请输入密码'}))

    #这是一种在LoginForm里的后台验证方法
    def clean(self):
        username = self.cleaned_data['username'] # 获取清洗后的用户名
        password = self.cleaned_data['password'] # 获取清洗后的密码
        user = auth.authenticate(username=username, password=password) # 用户认证的一种方法
        # 如果用户存在，登录，返回之前网页
        # 如果用户不存在，报错
        if user is None:
            raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data

# 创建Django表单类，用于注册
class RegForm(forms.Form):

    username = forms.CharField(label="用户名", max_length=30, min_length=3,\
                               widget=forms.TextInput(attrs= {'class':'form-control', 'placeholder':'请输入3-30位的用户名'})) # required默认是True
    email = forms.CharField(label="邮箱", \
                            widget=forms.EmailInput(attrs= {'class':'form-control', 'placeholder':'请输入邮箱'})) # required默认是True
    password = forms.CharField(label="密码", \
                               min_length=6, \
                               widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}))
    password_again = forms.CharField(label="再输一次密码", \
                                    min_length=6, \
                                    widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}))
    # 自动检测username是否存在
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).count() > 0:
            raise forms.ValidationError('用户名已存在')
        return username
    # 自动检测email是否存在
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError('邮箱已存在')
        return email
    # 自动检测两次password是否一样
    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('两次输入的密码不一致')
        return password_again

