from typing import Dict, Any, Optional
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from django.contrib.auth.hashers import check_password
from django.core.cache import cache
from django.contrib.auth import get_user_model
import logging

from users.views.base import ProtectedAPIView
from users.constants import (
    ResponseCode, ResponseMessage, SmsScene, 
    Limits, CacheKey
)
from users.views.mixins import ResponseMixin, ValidationMixin

User = get_user_model()
logger = logging.getLogger('users')

class ChangePasswordView(ProtectedAPIView, ResponseMixin, ValidationMixin):
    """修改密码视图"""
    
    def validate_password_change(
        self, 
        old_password: str,
        new_password: str,
        confirm_password: str
    ) -> Optional[Response]:
        """
        验证密码修改参数
        返回 None 表示验证通过，否则返回错误响应
        """
        # 验证必填字段
        if not all([old_password, new_password, confirm_password]):
            return self.error_response(
                message='请填写完整的密码信息',
                errors=self.get_empty_field_errors({
                    'old_password': old_password,
                    'new_password': new_password,
                    'confirm_password': confirm_password
                })
            )
        
        # 验证新密码长度
        if not self.validate_password_length(new_password):
            return self.error_response(
                message=f'新密码长度必须在{Limits.MIN_PASSWORD_LENGTH}-{Limits.MAX_PASSWORD_LENGTH}位之间',
                errors={'new_password': ['密码长度不符合要求']}
            )
        
        # 验证新密码一致性
        if new_password != confirm_password:
            return self.error_response(
                message='两次输入的新密码不一致',
                errors={'confirm_password': ['两次输入的密码不一致']}
            )
        
        # 验证新旧密码不同
        if old_password == new_password:
            return self.error_response(
                message='新密码不能与当前密码相同',
                errors={'new_password': ['新密码不能与当前密码相同']}
            )
            
        return None

    def post(self, request: Request) -> Response:
        """修改密码"""
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        
        # 参数验证
        validation_error = self.validate_password_change(
            old_password, new_password, confirm_password
        )
        if validation_error:
            return validation_error
        
        user = request.user
        
        # 验证当前密码
        if not user.check_password(old_password):
            return self.error_response(
                message='当前密码错误',
                errors={'old_password': ['当前密码错误']}
            )
        
        try:
            user.set_password(new_password)
            user.save()
            return self.success_response(message='密码修改成功')
            
        except Exception as e:
            logger.exception("密码修改失败")
            return self.error_response(
                message='密码修改失败，请重试',
                code=ResponseCode.SERVER_ERROR,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DeleteAccountView(ProtectedAPIView, ResponseMixin):
    """注销账号视图"""
    
    def post(self, request: Request) -> Response:
        """注销账号"""
        password = request.data.get('password')
        
        if not password:
            return self.error_response(
                message='请输入密码',
                errors={'password': ['此字段不能为空']}
            )
        
        user = request.user
        
        # 验证密码
        if not check_password(password, user.password):
            return self.error_response(
                message='密码错误',
                errors={'password': ['密码错误']}
            )
        
        try:
            user.delete()
            return self.success_response(message='账号已注销成功')
            
        except Exception as e:
            logger.exception("账号注销失败")
            return self.error_response(
                message='账号注销失败，请重试',
                code=ResponseCode.SERVER_ERROR,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ChangePhoneView(ProtectedAPIView, ResponseMixin, ValidationMixin):
    """更换手机号视图"""
    
    def validate_phone_change(
        self, 
        phone: str,
        code: str,
        user_id: int
    ) -> Optional[Response]:
        """验证手机号修改参数"""
        # 验证必填字段
        if not all([phone, code]):
            return self.error_response(
                message=ResponseMessage.INVALID_PARAMS,
                errors=self.get_empty_field_errors({
                    'phone': phone,
                    'code': code
                })
            )
        
        # 验证手机号格式
        if not self.validate_phone(phone):
            return self.error_response(
                message=ResponseMessage.INVALID_PARAMS,
                errors={'phone': ['请输入正确的手机号']}
            )
        
        # 验证手机号是否已被使用
        if User.objects.filter(phone=phone).exclude(id=user_id).exists():
            return self.error_response(
                message=ResponseMessage.USER_ALREADY_EXISTS,
                errors={'phone': ['该手机号已被使用']}
            )
            
        return None

    def post(self, request: Request) -> Response:
        """更换手机号"""
        phone = request.data.get('phone')
        code = request.data.get('code')
        
        # 参数验证
        validation_error = self.validate_phone_change(
            phone, code, request.user.id
        )
        if validation_error:
            return validation_error
        
        # 验证验证码
        cache_key = CacheKey.get_sms_code_key(SmsScene.CHANGE_PHONE, phone)
        cached_code = cache.get(cache_key)
        
        if not cached_code:
            return self.error_response(
                message=ResponseMessage.SMS_CODE_EXPIRED,
                errors={'code': ['验证码已过期']}
            )
        
        if cached_code != code:
            return self.error_response(
                message=ResponseMessage.SMS_CODE_INVALID,
                errors={'code': ['验证码错误']}
            )
        
        try:
            user = request.user
            user.phone = phone
            user.username = phone  # 如果用户名与手机号相同，也需要更新
            user.save()
            
            # 清除验证码缓存
            cache.delete(cache_key)
            
            return self.success_response(
                message='手机号更换成功',
                data={'phone': phone}
            )
            
        except Exception as e:
            logger.exception("更换手机号失败")
            return self.error_response(
                message=ResponseMessage.SERVER_ERROR,
                code=ResponseCode.SERVER_ERROR,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )