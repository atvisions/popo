# users/views.py
import logging
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import generate_code, send_sms
from .constants import (
    SmsScene, LoginMode, CacheKey, ResponseCode, 
    ResponseMessage, Limits, ErrorCode
)

# 配置日志
logger = logging.getLogger('users')
User = get_user_model()

class SendSmsCodeView(APIView):
    """发送验证码视图"""
    
    def post(self, request):
        phone = request.data.get('phone')
        scene = request.data.get('scene')
        login_mode = request.data.get('login_mode')
        
        # 参数验证
        if not phone:
            return Response({
                'code': ResponseCode.BAD_REQUEST,
                'message': ResponseMessage.INVALID_PARAMS,
                'errors': {'phone': ['手机号不能为空']}
            }, status=status.HTTP_400_BAD_REQUEST)
            
        if not SmsScene.is_valid(scene):
            return Response({
                'code': ResponseCode.BAD_REQUEST,
                'message': ResponseMessage.INVALID_PARAMS,
                'errors': {'scene': ['无效的场景类型']}
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # 登录场景需要验证登录模式
        if scene == SmsScene.LOGIN and not LoginMode.is_valid(login_mode):
            return Response({
                'code': ResponseCode.BAD_REQUEST,
                'message': ResponseMessage.INVALID_PARAMS,
                'errors': {'login_mode': ['无效的登录模式']}
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # 业务逻辑验证
        user_exists = User.objects.filter(phone=phone).exists()
        if scene == SmsScene.REGISTER and user_exists:
            return Response({
                'code': ResponseCode.BAD_REQUEST,
                'message': ResponseMessage.USER_ALREADY_EXISTS,
                'errors': {'phone': ['该手机号已注册']}
            }, status=status.HTTP_400_BAD_REQUEST)
            
        if scene in [SmsScene.LOGIN, SmsScene.RESET_PASSWORD] and not user_exists:
            return Response({
                'code': ResponseCode.NOT_FOUND,
                'message': ResponseMessage.USER_NOT_FOUND,
                'errors': {'phone': ['该手机号未注册']}
            }, status.HTTP_404_NOT_FOUND)
            
        # 生成验证码
        code = generate_code()
        success, message = send_sms(phone, code, scene)
        
        if not success:
            return Response({
                'code': ResponseCode.TOO_MANY_REQUESTS if 'flow_control' in message 
                    else ResponseCode.SERVER_ERROR,
                'message': message,
                'errors': {'system': [message]}
            }, status.HTTP_429_TOO_MANY_REQUESTS if 'flow_control' in message 
                else status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        # 保存验证码到缓存
        cache_key = CacheKey.get_sms_code_key(scene, phone)
        cache.set(cache_key, code, timeout=Limits.SMS_CODE_EXPIRE_MINUTES * 60)
        
        return Response({
            'code': ResponseCode.SUCCESS,
            'message': ResponseMessage.SMS_SEND_SUCCESS,
            'data': {
                'phone': phone,
                'scene': scene,
                'expire_minutes': Limits.SMS_CODE_EXPIRE_MINUTES
            }
        })
class PasswordLoginView(APIView):
    """密码登录视图"""
    
    def post(self, request):
        phone = request.data.get('phone')
        password = request.data.get('password')
        
        # 参数验证
        if not all([phone, password]):
            errors = {}
            if not phone:
                errors['phone'] = ['手机号不能为空']
            if not password:
                errors['password'] = ['密码不能为空']
                
            return Response({
                'code': ResponseCode.BAD_REQUEST,
                'message': ResponseMessage.INVALID_PARAMS,
                'errors': errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            # 查找用户
            user = User.objects.get(phone=phone)
            
            # 验证密码
            if not user.check_password(password):
                return Response({
                    'code': ResponseCode.BAD_REQUEST,
                    'message': ResponseMessage.INVALID_CREDENTIALS,
                    'errors': {'password': ['密码错误']}
                }, status=status.HTTP_400_BAD_REQUEST)
                
            # 生成token
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'code': ResponseCode.SUCCESS,
                'message': '登录成功',
                'data': {
                    'user': {
                        'id': user.id,
                        'phone': user.phone,
                        'username': user.username,
                        'created_time': user.created_time,
                    },
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }
            })
            
        except User.DoesNotExist:
            return Response({
                'code': ResponseCode.NOT_FOUND,
                'message': ResponseMessage.USER_NOT_FOUND,
                'errors': {'phone': ['用户不存在']}
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            logger.exception("密码登录异常")
            return Response({
                'code': ResponseCode.SERVER_ERROR,
                'message': ResponseMessage.SERVER_ERROR,
                'errors': {'system': [str(e)]}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class RegisterView(APIView):
    """用户注册视图"""
    
    def post(self, request):
        phone = request.data.get('phone')
        code = request.data.get('code')
        password = request.data.get('password')
        
        # 参数验证
        if not all([phone, code, password]):
            errors = {}
            if not phone:
                errors['phone'] = ['手机号不能为空']
            if not code:
                errors['code'] = ['验证码不能为空']
            if not password:
                errors['password'] = ['密码不能为空']
                
            return Response({
                'code': ResponseCode.BAD_REQUEST,
                'message': ResponseMessage.INVALID_PARAMS,
                'errors': errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # 验证手机号是否已注册
        if User.objects.filter(phone=phone).exists():
            return Response({
                'code': ResponseCode.BAD_REQUEST,
                'message': ResponseMessage.USER_ALREADY_EXISTS,
                'errors': {'phone': ['该手机号已注册']}
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # 验证码校验
        cache_key = CacheKey.get_sms_code_key(SmsScene.REGISTER, phone)
        cached_code = cache.get(cache_key)
        
        if not cached_code:
            return Response({
                'code': ResponseCode.BAD_REQUEST,
                'message': ResponseMessage.SMS_CODE_EXPIRED,
                'errors': {'code': ['验证码已过期']}
            }, status=status.HTTP_400_BAD_REQUEST)
            
        if cached_code != code:
            return Response({
                'code': ResponseCode.BAD_REQUEST,
                'message': ResponseMessage.SMS_CODE_INVALID,
                'errors': {'code': ['验证码错误']}
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # 创建用户
        try:
            user = User.objects.create_user(
                username=phone,
                phone=phone,
                password=password
            )
            
            # 清除验证码缓存
            cache.delete(cache_key)
            
            # 生成token
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'code': ResponseCode.SUCCESS,
                'message': '注册成功',
                'data': {
                    'user': {
                        'phone': user.phone,
                        'created_time': user.created_time,
                    },
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.exception("用户注册异常")
            return Response({
                'code': ResponseCode.SERVER_ERROR,
                'message': ResponseMessage.SERVER_ERROR,
                'errors': {'system': [str(e)]}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CodeLoginView(APIView):
    """验证码登录视图"""
    
    def post(self, request):
        phone = request.data.get('phone')
        code = request.data.get('code')
        
        # 参数验证
        if not all([phone, code]):
            errors = {}
            if not phone:
                errors['phone'] = ['手机号不能为空']
            if not code:
                errors['code'] = ['验证码不能为空']
                
            return Response({
                'code': ResponseCode.BAD_REQUEST,
                'message': ResponseMessage.INVALID_PARAMS,
                'errors': errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # 验证码校验
        cache_key = CacheKey.get_sms_code_key(SmsScene.LOGIN, phone)
        cached_code = cache.get(cache_key)
        
        if not cached_code:
            return Response({
                'code': ResponseCode.BAD_REQUEST,
                'message': ResponseMessage.SMS_CODE_EXPIRED,
                'errors': {'code': ['验证码已过期']}
            }, status=status.HTTP_400_BAD_REQUEST)
            
        if cached_code != code:
            return Response({
                'code': ResponseCode.BAD_REQUEST,
                'message': ResponseMessage.SMS_CODE_INVALID,
                'errors': {'code': ['验证码错误']}
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            # 获取或创建用户
            user, created = User.objects.get_or_create(
                phone=phone,
                defaults={'username': phone}
            )
            
            if created:
                # 为新用户设置随机密码
                user.set_password(User.objects.make_random_password())
                user.save()
                
            # 清除验证码缓存
            cache.delete(cache_key)
            
            # 生成token
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'code': ResponseCode.SUCCESS,
                'message': '登录成功',
                'data': {
                    'is_new_user': created,
                    'user': {
                        'phone': user.phone,
                        'created_time': user.created_time,
                    },
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }
            })
            
        except Exception as e:
            logger.exception("验证码登录异常")
            return Response({
                'code': ResponseCode.SERVER_ERROR,
                'message': ResponseMessage.SERVER_ERROR,
                'errors': {'system': [str(e)]}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ResetPasswordView(APIView):
    """重置密码视图"""
    
    def post(self, request):
        phone = request.data.get('phone')
        code = request.data.get('code')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        
        # 参数验证
        if not all([phone, code, new_password, confirm_password]):
            errors = {}
            if not phone:
                errors['phone'] = ['手机号不能为空']
            if not code:
                errors['code'] = ['验证码不能为空']
            if not new_password:
                errors['new_password'] = ['新密码不能为空']
            if not confirm_password:
                errors['confirm_password'] = ['确认密码不能为空']
                
            return Response({
                'code': ResponseCode.BAD_REQUEST,
                'message': ResponseMessage.INVALID_PARAMS,
                'errors': errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # 验证用户是否存在
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response({
                'code': ResponseCode.NOT_FOUND,
                'message': ResponseMessage.USER_NOT_FOUND,
                'errors': {'phone': ['用户不存在']}
            }, status=status.HTTP_404_NOT_FOUND)
            
        # 验证两次密码是否一致
        if new_password != confirm_password:
            return Response({
                'code': ResponseCode.BAD_REQUEST,
                'message': '两次密码不一致',
                'errors': {'confirm_password': ['两次输入的密码不一致']}
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # 验证密码长度
        if len(new_password) < Limits.MIN_PASSWORD_LENGTH:
            return Response({
                'code': ResponseCode.BAD_REQUEST,
                'message': '密码太短',
                'errors': {'new_password': [f'密码长度不能少于{Limits.MIN_PASSWORD_LENGTH}位']}
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # 验证验证码
        cache_key = CacheKey.get_sms_code_key(SmsScene.RESET_PASSWORD, phone)
        cached_code = cache.get(cache_key)
        
        if not cached_code:
            return Response({
                'code': ResponseCode.BAD_REQUEST,
                'message': ResponseMessage.SMS_CODE_EXPIRED,
                'errors': {'code': ['验证码已过期']}
            }, status=status.HTTP_400_BAD_REQUEST)
            
        if cached_code != code:
            return Response({
                'code': ResponseCode.BAD_REQUEST,
                'message': ResponseMessage.SMS_CODE_INVALID,
                'errors': {'code': ['验证码错误']}
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            # 更新密码
            user.set_password(new_password)
            user.save()
            
            # 清除验证码缓存
            cache.delete(cache_key)
            
            # 生成新的token
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'code': ResponseCode.SUCCESS,
                'message': '密码重置成功',
                'data': {
                    'user': {
                        'phone': user.phone
                    },
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token)
                    }
                }
            })
            
        except Exception as e:
            logger.exception("重置密码异常")
            return Response({
                'code': ResponseCode.SERVER_ERROR,
                'message': ResponseMessage.SERVER_ERROR,
                'errors': {'system': [str(e)]}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)