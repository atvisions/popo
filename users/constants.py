class SmsScene:
    """短信场景"""
    REGISTER = 'register'
    LOGIN = 'login'
    RESET_PASSWORD = 'reset_password'

    CHOICES = {
        REGISTER: '注册',
        LOGIN: '登录',
        RESET_PASSWORD: '重置密码'
    }

    @classmethod
    def is_valid(cls, scene):
        """验证场景是否有效"""
        return scene in cls.CHOICES

class LoginMode:
    """登录模式"""
    PASSWORD = 'password'
    CODE = 'code'

    CHOICES = {
        PASSWORD: '密码登录',
        CODE: '验证码登录'
    }

    @classmethod
    def is_valid(cls, mode):
        """验证登录模式是否有效"""
        return mode in cls.CHOICES

class CacheKey:
    """缓存键模板"""
    SMS_CODE = '{scene}_code_{phone}'  # 短信验证码
    LOGIN_ATTEMPTS = 'login_attempts_{phone}'  # 登录尝试次数
    USER_TOKENS = 'user_tokens_{user_id}'  # 用户token

    @classmethod
    def get_sms_code_key(cls, scene, phone):
        """获取短信验证码的缓存键"""
        return cls.SMS_CODE.format(scene=scene, phone=phone)

    @classmethod
    def get_login_attempts_key(cls, phone):
        """获取登录尝试次数的缓存键"""
        return cls.LOGIN_ATTEMPTS.format(phone=phone)

class ResponseCode:
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
    SERVER_ERROR = "服务器错误"
    
    # 用户相关
    USER_NOT_FOUND = "用户不存在"
    USER_ALREADY_EXISTS = "用户已存在"
    INVALID_CREDENTIALS = "账号或密码错误"
    
    # 验证码相关
    SMS_SEND_SUCCESS = "验证码发送成功"
    SMS_SEND_FAILED = "验证码发送失败"
    SMS_CODE_EXPIRED = "验证码已过期"
    SMS_CODE_INVALID = "验证码错误"
    SMS_RATE_LIMIT = "发送太频繁，请稍后再试"

class Limits:
    """限制配置"""
    # 短信相关
    SMS_CODE_LENGTH = 6  # 验证码长度
    SMS_CODE_EXPIRE_MINUTES = 5  # 验证码有效期（分钟）
    SMS_HOUR_LIMIT = 5  # 每小时最大发送次数
    SMS_DAY_LIMIT = 20  # 每天最大发送次数
    
    # 密码相关
    MIN_PASSWORD_LENGTH = 6  # 最小密码长度
    MAX_PASSWORD_LENGTH = 20  # 最大密码长度
    
    # 登录相关
    MAX_LOGIN_ATTEMPTS = 5  # 最大登录尝试次数
    LOGIN_ATTEMPTS_EXPIRE_MINUTES = 30  # 登录锁定时间（分钟）

class RegexPattern:
    """正则表达式模式"""
    PHONE = r'^1[3-9]\d{9}$'  # 手机号
    PASSWORD = r'^[a-zA-Z0-9@#$%^&+=]{6,20}$'  # 密码

class ErrorCode:
    """错误代码"""
    INVALID_PHONE = 'invalid_phone'
    INVALID_PASSWORD = 'invalid_password'
    INVALID_CODE = 'invalid_code'
    USER_NOT_FOUND = 'user_not_found'
    USER_EXISTS = 'user_exists'
    RATE_LIMIT = 'rate_limit'
    SYSTEM_ERROR = 'system_error'