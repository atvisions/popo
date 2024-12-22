from enum import Enum
from typing import Dict, ClassVar

class SmsScene:
    """短信验证码场景"""
    REGISTER = 'register'         # 注册
    LOGIN = 'login'              # 登录
    RESET_PASSWORD = 'reset_password'     # 重置密码
    CHANGE_PHONE = 'change_phone'        # 更换手机号

    CHOICES: ClassVar[Dict[str, str]] = {
        REGISTER: '注册',
        LOGIN: '登录',
        RESET_PASSWORD: '重置密码',
        CHANGE_PHONE: '更换手机号'
    }

    @classmethod
    def is_valid(cls, scene: str) -> bool:
        """验证场景是否有效"""
        return scene in cls.CHOICES

class LoginMode(Enum):
    """登录模式"""
    PASSWORD = 'password'  # 密码登录
    CODE = 'code'         # 验证码登录

    @classmethod
    def get_choices(cls) -> Dict[str, str]:
        return {
            cls.PASSWORD.value: '密码登录',
            cls.CODE.value: '验证码登录'
        }

    @classmethod
    def is_valid(cls, mode: str) -> bool:
        """验证登录模式是否有效"""
        return mode in [item.value for item in cls]

class CacheKey:
    """缓存键模板"""
    # 缓存键前缀
    PREFIX = 'users'
    
    # 短信相关
    SMS_CODE = f'{PREFIX}:sms:code:{{scene}}:{{phone}}'  # 短信验证码
    SMS_HOUR_LIMIT = f'{PREFIX}:sms:hour:{{phone}}'      # 小时发送次数
    SMS_DAY_LIMIT = f'{PREFIX}:sms:day:{{phone}}'        # 每日发送次数
    
    # 登录相关
    LOGIN_ATTEMPTS = f'{PREFIX}:login:attempts:{{phone}}'  # 登录尝试次数
    USER_TOKENS = f'{PREFIX}:tokens:{{user_id}}'          # 用户token

    @classmethod
    def get_sms_code_key(cls, scene: str, phone: str) -> str:
        """获取短信验证码的缓存键"""
        return cls.SMS_CODE.format(scene=scene, phone=phone)

    @classmethod
    def get_sms_hour_limit_key(cls, phone: str) -> str:
        """获取短信小时限制的缓存键"""
        return cls.SMS_HOUR_LIMIT.format(phone=phone)

    @classmethod
    def get_sms_day_limit_key(cls, phone: str) -> str:
        """获取短信每日限制的缓存键"""
        return cls.SMS_DAY_LIMIT.format(phone=phone)

    @classmethod
    def get_login_attempts_key(cls, phone: str) -> str:
        """获取登录尝试次数的缓存键"""
        return cls.LOGIN_ATTEMPTS.format(phone=phone)

    @classmethod
    def get_user_tokens_key(cls, user_id: int) -> str:
        """获取用户token的缓存键"""
        return cls.USER_TOKENS.format(user_id=user_id)

class ResponseCode(Enum):
    """响应状态码"""
    SUCCESS = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    TOO_MANY_REQUESTS = 429
    SERVER_ERROR = 500

class ResponseMessage:
    """响应消息"""
    SUCCESS = "操作成功"
    INVALID_PARAMS = "无效的参数"
    SERVER_ERROR = "服务器错误，请稍后重试"
    
    # 用户相关
    USER_NOT_FOUND = "用户不存在"
    USER_ALREADY_EXISTS = "用户已存在"
    INVALID_CREDENTIALS = "账号或密码错误"
    ACCOUNT_LOCKED = "账号已被锁定，请稍后再试"
    
    # 验证码相关
    SMS_SEND_SUCCESS = "验证码发送成功"
    SMS_SEND_FAILED = "验证码发送失败"
    SMS_CODE_EXPIRED = "验证码已过期"
    SMS_CODE_INVALID = "验证码错误"
    SMS_RATE_LIMIT = "发送太频繁，请稍后再试"

    # 权限相关
    PERMISSION_DENIED = "权限不足"
    TOKEN_INVALID = "无效的令牌"
    TOKEN_EXPIRED = "令牌已过期"

    # 密码相关
    INVALID_PASSWORD_FORMAT = '密码必须包含字母和数字，且不少于8位'

class Limits:
    """系统限制配置"""
    # 短信相关
    SMS_CODE_LENGTH: int = 6  # 验证码长度
    SMS_CODE_EXPIRE_MINUTES: int = 5  # 验证码有效期（分钟）
    SMS_HOUR_LIMIT: int = 5  # 每小时最大发送次数
    SMS_DAY_LIMIT: int = 10  # 每天最大发送次数
    
    # 密码相关
    MIN_PASSWORD_LENGTH: int = 8  # 最小密码长度
    MAX_PASSWORD_LENGTH: int = 20  # 最大密码长度
    
    # 登录相关
    MAX_LOGIN_ATTEMPTS: int = 5  # 最大登录尝试次数
    LOGIN_ATTEMPTS_EXPIRE_MINUTES: int = 30  # 登录锁定时间（分钟）
    
    # Token相关
    ACCESS_TOKEN_LIFETIME_MINUTES: int = 30  # 访问令牌有效期
    REFRESH_TOKEN_LIFETIME_DAYS: int = 7  # 刷新令牌有效期

class RegexPattern:
    """正则表达式模式"""
    PHONE = r'^1[3-9]\d{9}$'  # 手机号
    PASSWORD = r'^[a-zA-Z0-9@#$%^&+=]{6,20}$'  # 密码
    USERNAME = r'^[a-zA-Z0-9_-]{3,16}$'  # 用户名

class ErrorCode(Enum):
    """错误代码"""
    INVALID_PHONE = 'invalid_phone'
    INVALID_PASSWORD = 'invalid_password'
    INVALID_CODE = 'invalid_code'
    USER_NOT_FOUND = 'user_not_found'
    USER_EXISTS = 'user_exists'
    RATE_LIMIT = 'rate_limit'
    SYSTEM_ERROR = 'system_error'
    PERMISSION_DENIED = 'permission_denied'
    TOKEN_INVALID = 'token_invalid'
    TOKEN_EXPIRED = 'token_expired'