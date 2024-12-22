from django.urls import path, include
from users.views.auth import (
    SendSmsCodeView,
    RegisterView,
    PasswordLoginView,
    CodeLoginView,
    LogoutView,
    ResetPasswordView,
    TokenRefreshView
)
from users.views.profile import (
    UserProfileView,
    AvatarUploadView
)
from users.views.account import (  # 导入账户管理视图
    ChangePasswordView,
    ChangePhoneView,
    DeleteAccountView
)

API_VERSION = 'v1'

# 认证相关路由
auth_patterns = [
    path('sms/send/', SendSmsCodeView.as_view(), name='send_sms'), # 发送短信验证码
    path('register/', RegisterView.as_view(), name='register'), # 注册  
    path('login/password/', PasswordLoginView.as_view(), name='password_login'), # 密码登录
    path('login/code/', CodeLoginView.as_view(), name='code_login'), # 验证码登录
    path('logout/', LogoutView.as_view(), name='logout'), # 登出
    path('password/reset/', ResetPasswordView.as_view(), name='reset_password'), # 重置密码
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 添加刷新token路由
]

# 用户资料相关路由
profile_patterns = [
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('profile/avatar/', AvatarUploadView.as_view(), name='upload_avatar'),
]

# 账户管理相关路由
account_patterns = [
    path('password/', ChangePasswordView.as_view(), name='change_password'), # 修改密码
    path('phone/', ChangePhoneView.as_view(), name='change_phone'), # 修改手机号
    path('delete/', DeleteAccountView.as_view(), name='delete_account'), # 删除账户
]

# URL patterns
urlpatterns = [
    # 认证相关路由
    path(f'{API_VERSION}/auth/', include(auth_patterns)),
    # 用户资料相关路由
    path(f'{API_VERSION}/users/', include(profile_patterns)),
    # 账户管理相关路由
    path(f'{API_VERSION}/users/account/', include(account_patterns)),
]