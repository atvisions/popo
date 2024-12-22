from typing import Dict, Any, Optional
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.views import TokenRefreshView as JWTTokenRefreshView
from django.contrib.auth import get_user_model
from django.core.cache import cache
import logging

from users.views.base import PublicAPIView, ProtectedAPIView
from users.views.mixins import (
    ResponseMixin,
    ValidationMixin,
    CacheMixin,
    LoggerMixin,
)
from users.constants import (
    ResponseCode,
    ResponseMessage,
    SmsScene,
    Limits,
    CacheKey
)
from users.utils import generate_code, send_sms

logger = logging.getLogger('users')
User = get_user_model()

class SendSmsCodeView(PublicAPIView, ResponseMixin, ValidationMixin, CacheMixin, LoggerMixin):
    """发送短信验证码视图"""
    renderer_classes = [JSONRenderer] 
    def validate_send_sms(
        self, 
        phone: str,
        scene: str
    ) -> Optional[Response]:
        """
        验证发送短信参数
        :param phone: 手机号
        :param scene: 场景
        :return: 错误响应或 None
        """
        # 验证必填参数
        if not all([phone, scene]):
            return self.error_response(
                message=ResponseMessage.INVALID_PARAMS,
                errors=self.get_empty_field_errors({
                    'phone': phone,
                    'scene': scene
                })
            )

        # 验证手机号格式
        if not self.validate_phone(phone):
            return self.error_response(
                message=ResponseMessage.INVALID_PARAMS,
                errors={'phone': ['请输入正确的手机号']}
            )

        # 验证场景
        if not SmsScene.is_valid(scene):
            return self.error_response(
                message=ResponseMessage.INVALID_PARAMS,
                errors={'scene': ['无效的场景']}
            )

        # 验证发送频率
        cache_key = CacheKey.get_sms_code_key(scene, phone)
        if self.get_cache(cache_key):
            return self.error_response(
                message=ResponseMessage.SMS_RATE_LIMIT,
                code=ResponseCode.TOO_MANY_REQUESTS,
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        # 根据场景验证用户状态
        if scene in [SmsScene.REGISTER, SmsScene.CHANGE_PHONE]:
            # 注册和更换手机号场景：验证手机号不存在
            if User.objects.filter(phone=phone).exists():
                return self.error_response(
                    message=ResponseMessage.USER_ALREADY_EXISTS,
                    errors={'phone': ['该手机号已被使用']}
                )
        else:
            # 其他场景（登录、重置密码）：验证用户存在
            if not User.objects.filter(phone=phone).exists():
                return self.error_response(
                    message=ResponseMessage.USER_NOT_FOUND,
                    errors={'phone': ['用户不存在']},
                    code=ResponseCode.NOT_FOUND,
                    status=status.HTTP_404_NOT_FOUND
                )

        return None

    def check_send_limits(self, phone: str) -> Optional[Response]:
        """
        检查发送频率限制
        :param phone: 手机号
        :return: 错误响应或 None
        """
        # 检查小时限制
        hour_key = CacheKey.get_sms_hour_limit_key(phone)
        hour_count = int(self.get_cache(hour_key) or 0)
        if hour_count >= Limits.SMS_HOUR_LIMIT:
            return self.error_response(
                message=ResponseMessage.SMS_RATE_LIMIT,
                code=ResponseCode.TOO_MANY_REQUESTS,
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        # 检查天限制
        day_key = CacheKey.get_sms_day_limit_key(phone)
        day_count = int(self.get_cache(day_key) or 0)
        if day_count >= Limits.SMS_DAY_LIMIT:
            return self.error_response(
                message='今日发送次数已达上限',
                code=ResponseCode.TOO_MANY_REQUESTS,
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        return None

    def update_send_limits(self, phone: str):
        """
        更新发送次数限制
        :param phone: 手机号
        """
        # 更新小时限制
        hour_key = CacheKey.get_sms_hour_limit_key(phone)
        hour_count = int(self.get_cache(hour_key) or 0)
        self.set_cache(hour_key, hour_count + 1, timeout=3600)  # 1小时

        # 更新天限制
        day_key = CacheKey.get_sms_day_limit_key(phone)
        day_count = int(self.get_cache(day_key) or 0)
        self.set_cache(day_key, day_count + 1, timeout=86400)  # 24小时

    def post(self, request: Request) -> Response:
        """发送短信验证码"""
        phone = request.data.get('phone')
        scene = request.data.get('scene')

        # 参数验证
        validation_error = self.validate_send_sms(phone, scene)
        if validation_error:
            return validation_error

        # 检查发送频率限制
        limit_error = self.check_send_limits(phone)
        if limit_error:
            return limit_error

        try:
            # 生成验证码
            code = generate_code(length=Limits.SMS_CODE_LENGTH)
            
            # 发送短信
            success = send_sms(phone, code, scene)
            if not success:
                return self.error_response(
                    message=ResponseMessage.SMS_SEND_FAILED,
                    code=ResponseCode.SERVER_ERROR,
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # 更新发送次数限制
            self.update_send_limits(phone)

            # 保存验证码到缓存
            cache_key = CacheKey.get_sms_code_key(scene, phone)
            self.set_cache(
                key=cache_key,
                value=code,
                timeout=Limits.SMS_CODE_EXPIRE_MINUTES * 60
            )

            return self.success_response(
                message=ResponseMessage.SMS_SEND_SUCCESS,
                data={
                    'phone': phone,
                    'scene': scene,
                    'expire_minutes': Limits.SMS_CODE_EXPIRE_MINUTES
                }
            )

        except Exception as e:
            self.log_error(f"发送短信验证码失败: {str(e)}")
            return self.error_response(
                message=ResponseMessage.SERVER_ERROR,
                code=ResponseCode.SERVER_ERROR,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AuthMixin(ResponseMixin):
    """认证相关通用方法"""
    
    def generate_tokens(self, user) -> Dict[str, str]:
        """生成访问令牌和刷新令牌"""
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def get_user_data(self, user) -> Dict[str, Any]:
        """获取用户基本信息"""
        return {
            'id': user.id,
            'phone': user.phone,
            'username': user.username,
            'created_time': user.created_time,
        }

    def generate_auth_response(
        self, 
        user, 
        message: str = '登录成功',
        extra_data: Dict = None
    ) -> Response:
        """生成认证响应"""
        response_data = {
            'user': self.get_user_data(user),
            'tokens': self.generate_tokens(user)
        }
        
        if extra_data:
            response_data.update(extra_data)
            
        return self.success_response(
            message=message,
            data=response_data
        )

class PasswordLoginView(PublicAPIView, AuthMixin, ValidationMixin):
    """密码登录视图"""
    
    def validate_login_params(
        self, 
        phone: str,
        password: str
    ) -> Optional[Response]:
        """验证登录参数"""
        # 验证必填字段
        if not all([phone, password]):
            return self.error_response(
                message=ResponseMessage.INVALID_PARAMS,
                errors=self.get_empty_field_errors({
                    'phone': phone,
                    'password': password
                })
            )
            
        # 验证手机号格式
        if not self.validate_phone(phone):
            return self.error_response(
                message=ResponseMessage.INVALID_PARAMS,
                errors={'phone': ['请输入正确的手机号']}
            )
            
        return None

    def post(self, request: Request) -> Response:
        phone = request.data.get('phone')
        password = request.data.get('password')
        
        # 参数验证
        validation_error = self.validate_login_params(phone, password)
        if validation_error:
            return validation_error
            
        try:
            # 查找用户
            user = User.objects.get(phone=phone)
            
            # 验证密码
            if not user.check_password(password):
                return self.error_response(
                    message=ResponseMessage.INVALID_CREDENTIALS,
                    errors={'password': ['密码错误']}
                )
            
            # 检查账号状态
            if not user.is_active:
                return self.error_response(
                    message=ResponseMessage.ACCOUNT_LOCKED,
                    code=ResponseCode.FORBIDDEN,
                    status=status.HTTP_403_FORBIDDEN
                )
                
            # 生成登录响应
            return self.generate_auth_response(user)
            
        except User.DoesNotExist:
            return self.error_response(
                message=ResponseMessage.USER_NOT_FOUND,
                errors={'phone': ['用户不存在']},
                code=ResponseCode.NOT_FOUND,
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.exception("登录失败")
            return self.error_response(
                message=ResponseMessage.SERVER_ERROR,
                code=ResponseCode.SERVER_ERROR,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class LogoutView(ProtectedAPIView, ResponseMixin):
    """登出视图"""
    
    def post(self, request: Request) -> Response:
        refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            return self.error_response(
                message='缺少刷新令牌',
                errors={'refresh': ['刷新令牌不能为空']}
            )
            
        try:
            # 将令牌加入黑名单
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return self.success_response(message='登出成功')
            
        except TokenError:
            return self.error_response(
                message='无效的刷新令牌',
                code=ResponseCode.UNAUTHORIZED,
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            logger.exception("登出失败")
            return self.error_response(
                message=ResponseMessage.SERVER_ERROR,
                code=ResponseCode.SERVER_ERROR,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CodeLoginView(PublicAPIView, AuthMixin, ValidationMixin, CacheMixin):
    """验证码登录视图"""
    
    def validate_code_login(
        self, 
        phone: str,
        code: str
    ) -> Optional[Response]:
        """验证登录参数"""
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
                errors={'phone': ['请输入正确的手机���']}
            )
            
        # 验证验证码
        cache_key = CacheKey.get_sms_code_key(SmsScene.LOGIN, phone)
        cached_code = self.get_cache(cache_key)
        
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
            
        return None

    def post(self, request: Request) -> Response:
        """验证码登录"""
        phone = request.data.get('phone')
        code = request.data.get('code')
        
        # 参数验证
        validation_error = self.validate_code_login(phone, code)
        if validation_error:
            return validation_error
            
        try:
            # 获取或创建用户
            user, created = User.objects.get_or_create(
                phone=phone,
                defaults={
                    'username': phone,
                    'is_active': True
                }
            )
            
            # 清除验证码缓存
            cache_key = CacheKey.get_sms_code_key(SmsScene.LOGIN, phone)
            self.delete_cache(cache_key)
            
            # 生成登录响应
            return self.generate_auth_response(
                user,
                message='登录成功',
                extra_data={'is_new_user': created}
            )
            
        except Exception as e:
            logger.exception("验证码登录失败")
            return self.error_response(
                message=ResponseMessage.SERVER_ERROR,
                code=ResponseCode.SERVER_ERROR,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class RegisterView(PublicAPIView, AuthMixin, ValidationMixin, CacheMixin):
    """注册视图"""
    
    def validate_register(
        self, 
        phone: str,
        code: str,
        password: str,
        confirm_password: str
    ) -> Optional[Response]:
        """验证注册参数"""
        # 验证必填字段
        if not all([phone, code, password, confirm_password]):
            return self.error_response(
                message=ResponseMessage.INVALID_PARAMS,
                errors=self.get_empty_field_errors({
                    'phone': phone,
                    'code': code,
                    'password': password,
                    'confirm_password': confirm_password
                })
            )
            
        # 验证手机号格式
        if not self.validate_phone(phone):
            return self.error_response(
                message=ResponseMessage.INVALID_PARAMS,
                errors={'phone': ['请输入正确的手机号']}
            )
            
        # 验证手机号是否已注册
        if User.objects.filter(phone=phone).exists():
            return self.error_response(
                message=ResponseMessage.USER_ALREADY_EXISTS,
                errors={'phone': ['该手机号已注册']}
            )
            
        # 验证密码
        if not self.validate_password(password):
            return self.error_response(
                message=ResponseMessage.INVALID_PASSWORD_FORMAT,
                errors={'password': ['密码必须包含字母和数字，且不少于8位']}
            )
            
        # 验证两次密码是否一致
        if password != confirm_password:
            return self.error_response(
                message='两次输入的密码不一致',
                errors={'confirm_password': ['两次输入的密码不一致']}
            )
            
        # 验证验证码
        cache_key = CacheKey.get_sms_code_key(SmsScene.REGISTER, phone)
        cached_code = self.get_cache(cache_key)
        
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
            
        return None

    def post(self, request: Request) -> Response:
        """注册新用户"""
        phone = request.data.get('phone')
        code = request.data.get('code')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        
        # 参数验证
        validation_error = self.validate_register(
            phone, code, password, confirm_password
        )
        if validation_error:
            return validation_error
            
        try:
            # 创建新用户
            user = User.objects.create_user(
                username=phone,
                phone=phone,
                password=password,
                is_active=True
            )
            
            # 清除验证码缓存
            cache_key = CacheKey.get_sms_code_key(SmsScene.REGISTER, phone)
            self.delete_cache(cache_key)
            
            # 生成登录响应
            return self.generate_auth_response(
                user,
                message='注册成功'
            )
            
        except Exception as e:
            logger.exception("注册失败")
            return self.error_response(
                message=ResponseMessage.SERVER_ERROR,
                code=ResponseCode.SERVER_ERROR,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class ResetPasswordView(PublicAPIView, AuthMixin, ValidationMixin, CacheMixin):
    """重置密码视图"""
    
    def validate_reset_password(
        self, 
        phone: str,
        code: str,
        new_password: str,
        confirm_password: str
    ) -> Optional[Response]:
        """验证重置密码参数"""
        # 验证必��字段
        if not all([phone, code, new_password, confirm_password]):
            return self.error_response(
                message=ResponseMessage.INVALID_PARAMS,
                errors=self.get_empty_field_errors({
                    'phone': phone,
                    'code': code,
                    'new_password': new_password,
                    'confirm_password': confirm_password
                })
            )
            
        # 验证手机号格式
        if not self.validate_phone(phone):
            return self.error_response(
                message=ResponseMessage.INVALID_PARAMS,
                errors={'phone': ['请输入正确的手机号']}
            )
            
        # 验证用户是否存在
        try:
            User.objects.get(phone=phone)
        except User.DoesNotExist:
            return self.error_response(
                message=ResponseMessage.USER_NOT_FOUND,
                errors={'phone': ['用户不存在']},
                code=ResponseCode.NOT_FOUND,
                status=status.HTTP_404_NOT_FOUND
            )
            
        # 验证密码
        if not self.validate_password(new_password):
            return self.error_response(
                message=ResponseMessage.INVALID_PASSWORD_FORMAT,
                errors={'new_password': ['密码必须包含字母和数字，且不少于8位']}
            )
            
        # 验证两次密码是否一致
        if new_password != confirm_password:
            return self.error_response(
                message='两次输入的密码不一致',
                errors={'confirm_password': ['两次输入的密码不一致']}
            )
            
        # 验证验证码
        cache_key = CacheKey.get_sms_code_key(SmsScene.RESET_PASSWORD, phone)
        cached_code = self.get_cache(cache_key)
        
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
            
        return None

    def post(self, request: Request) -> Response:
        """重置密码"""
        phone = request.data.get('phone')
        code = request.data.get('code')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        
        # 参数验证
        validation_error = self.validate_reset_password(
            phone, code, new_password, confirm_password
        )
        if validation_error:
            return validation_error
            
        try:
            # 更新密码
            user = User.objects.get(phone=phone)
            user.set_password(new_password)
            user.save()
            
            # 清除验证码缓存
            cache_key = CacheKey.get_sms_code_key(SmsScene.RESET_PASSWORD, phone)
            self.delete_cache(cache_key)
            
            # 生成登录响应
            return self.generate_auth_response(
                user,
                message='密码重置成功'
            )
            
        except User.DoesNotExist:
            return self.error_response(
                message=ResponseMessage.USER_NOT_FOUND,
                code=ResponseCode.NOT_FOUND,
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.exception("重置密码失败")
            return self.error_response(
                message=ResponseMessage.SERVER_ERROR,
                code=ResponseCode.SERVER_ERROR,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class TokenRefreshView(JWTTokenRefreshView):
    """
    刷新访问令牌
    """
    def post(self, request, *args, **kwargs):
        try:
            print("Token refresh request data:", request.data)
            
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({
                    'code': 400,
                    'message': '缺少刷新令牌',
                    'detail': 'No refresh token provided'
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                # 解析 token
                token = RefreshToken(refresh_token)
                
                # 获取用户 ID
                user_id = token.payload.get('user_id')
                if not user_id:
                    raise InvalidToken('Token contains no user id')
                
                # 获取用户对象
                try:
                    user = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    raise InvalidToken('User not found')

                # 检查 token 是否在黑名单中
                if token.check_blacklist():
                    return Response({
                        'code': 400,
                        'message': '令牌已失效',
                        'detail': 'Token is blacklisted'
                    }, status=status.HTTP_400_BAD_REQUEST)

                # 生成新的 access token
                access_token = str(token.access_token)
                
                # 生成新的 refresh token
                new_refresh = RefreshToken.for_user(user)
                
                # 将旧的 refresh token 加入黑名单
                token.blacklist()
                
                response_data = {
                    'code': 200,
                    'message': '刷新成功',
                    'access': access_token,
                    'refresh': str(new_refresh)
                }
                
                print("Token refresh successful:", {
                    'user_id': user_id,
                    'new_token_issued': True
                })
                
                return Response(response_data)
                
            except TokenError as e:
                print("Token validation error:", str(e))
                return Response({
                    'code': 400,
                    'message': '令牌无效',
                    'detail': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            print("Unexpected error:", str(e))
            return Response({
                'code': 400,
                'message': '刷新失败',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)