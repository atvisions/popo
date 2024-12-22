# 认证相关视图
from .auth import (
    SendSmsCodeView,
    PasswordLoginView,
    CodeLoginView,
    RegisterView,
    LogoutView,
    ResetPasswordView
)

# 用户资料相关视图
from .profile import (
    UserProfileView,
    AvatarUploadView
)

# 账号管理相关视图
from .account import (
    ChangePasswordView,
    DeleteAccountView,
    ChangePhoneView
)

# 导出所有视图
__all__ = [
    # 认证相关
    'SendSmsCodeView',
    'PasswordLoginView',
    'CodeLoginView',
    'RegisterView',
    'LogoutView',
    'ResetPasswordView',
    
    # 用户资料相关
    'UserProfileView',
    'AvatarUploadView',
    
    # 账号管理相关
    'ChangePasswordView',
    'DeleteAccountView',
    'ChangePhoneView',
]