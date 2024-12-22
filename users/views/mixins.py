from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from users.constants import ResponseCode, ResponseMessage, Limits
import re
from typing import Dict, Any, Optional
from django.core.cache import cache

class TokenMixin:
    """Token 相关方法"""
    def generate_tokens(self, user):
        """生成访问令牌和刷新令牌"""
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def generate_auth_response(self, user, message='登录成功', extra_data=None):
        """生成带有用户信息和令牌的认证响应"""
        tokens = self.generate_tokens(user)
        response_data = {
            'code': ResponseCode.SUCCESS,
            'message': message,
            'data': {
                'user': {
                    'id': user.id,
                    'phone': user.phone,
                    'username': user.username,
                    'created_time': user.created_time,
                },
                'tokens': tokens
            }
        }
        
        if extra_data:
            response_data['data'].update(extra_data)
            
        return Response(response_data)

class ResponseMixin:
    """响应相关方法"""
    def success_response(
        self, 
        message: str = '操作成功', 
        data: Optional[Dict[str, Any]] = None, 
        status: int = 200
    ) -> Response:
        """
        成功响应
        :param message: 响应消息
        :param data: 响应数据
        :param status: HTTP状态码
        :return: Response 对象
        """
        response_data = {
            'code': 0,
            'message': message
        }
        if data is not None:
            response_data['data'] = data
        return Response(response_data, status=status)

    def error_response(
        self, 
        message: str, 
        errors: Optional[Dict[str, Any]] = None, 
        code: int = 400,
        status: int = 400
    ) -> Response:
        """
        错误响应
        :param message: 错误消息
        :param errors: 详细错误信息
        :param code: 错误代码
        :param status: HTTP状态码
        :return: Response 对象
        """
        response_data = {
            'code': code,
            'message': message
        }
        if errors:
            response_data['errors'] = errors
        return Response(response_data, status=status)

class ValidationMixin:
    """验证相关方法"""
    def validate_required_fields(self, data, required_fields):
        """验证必填字段"""
        errors = {}
        for field in required_fields:
            if not data.get(field):
                errors[field] = [f'{field}不能为空']
        return errors

    def validate_phone(self, phone: str) -> bool:
        """
        验证手机号格式
        :param phone: 手机号
        :return: 是否有效
        """
        if not phone:
            return False
        return bool(re.match(r'^1[3-9]\d{9}$', phone))

    def validate_password_length(self, password: str) -> bool:
        """
        验证密码长度
        :param password: 密码
        :return: 是否有效
        """
        if not password:
            return False
        return len(password) >= 8

    def get_empty_field_errors(self, fields: Dict[str, Any]) -> Dict[str, list]:
        """
        获取空字段错误信息
        :param fields: 字段字典
        :return: 错误信息字典
        """
        errors = {}
        for field, value in fields.items():
            if not value:
                errors[field] = ['此字段不能为空']
        return errors

    def validate_password(self, password: str) -> bool:
        """
        验证密码格式
        要求：
        1. 长度至少8位
        2. 必须包含字母和数字
        :param password: 密码
        :return: 是否有效
        """
        if not password:
            return False
        
        # 验证密码长度
        if len(password) < 8:
            return False
        
        # 验证必须包含字母和数字
        has_digit = any(char.isdigit() for char in password)
        has_letter = any(char.isalpha() for char in password)
        
        return has_digit and has_letter

class CacheMixin:
    """缓存相关方法"""
    def get_cache_key(self, prefix, *args):
        """生成缓存键"""
        return f"{prefix}:{'_'.join(map(str, args))}"

    def set_cache(self, key, value, timeout=None):
        """设置缓存"""
        from django.core.cache import cache
        cache.set(key, value, timeout)

    def get_cache(self, key):
        """获取缓存"""
        from django.core.cache import cache
        return cache.get(key)

    def delete_cache(self, key):
        """删除缓存"""
        from django.core.cache import cache
        cache.delete(key)

class LoggerMixin:
    """日志相关方法"""
    @property
    def logger(self):
        """获取日志记录器"""
        import logging
        return logging.getLogger('users')

    def log_error(self, message, exc_info=True):
        """记录错误日志"""
        self.logger.error(message, exc_info=exc_info)

    def log_info(self, message):
        """记录信息日志"""
        self.logger.info(message)

    def log_debug(self, message):
        """记录调试日志"""
        self.logger.debug(message)