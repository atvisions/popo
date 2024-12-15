# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # 发送验证码
    path('sms/code/', views.SendSmsCodeView.as_view(), name='send_sms'),
    
    # 用户注册
    path('register/', views.RegisterView.as_view(), name='register'),
    
    # 密码登录
    path('login/password/', views.PasswordLoginView.as_view(), name='login_password'),
    
    # 验证码登录
    path('login/code/', views.CodeLoginView.as_view(), name='login_code'),
    
    # 重置密码
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset_password'),
]