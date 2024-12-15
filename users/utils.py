# users/utils.py
import random
import logging
from django.conf import settings
from alibabacloud_dysmsapi20170525.client import Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_models
from .constants import SmsScene, Limits, ResponseMessage

# 配置日志
logger = logging.getLogger('sms')

def generate_code(length=Limits.SMS_CODE_LENGTH):
    """
    生成指定长度的数字验证码
    :param length: 验证码长度，默认6位
    :return: 验证码字符串
    """
    return ''.join(random.choices('0123456789', k=length))

def get_sms_client():
    """
    获取阿里云短信客户端
    :return: 阿里云短信客户端实例
    """
    try:
        config = open_api_models.Config(
            access_key_id=settings.ALIYUN_ACCESS_KEY_ID,
            access_key_secret=settings.ALIYUN_ACCESS_KEY_SECRET
        )
        config.endpoint = 'dysmsapi.aliyuncs.com'
        return Client(config)
    except Exception as e:
        logger.error(f"初始化短信客户端失败: {str(e)}")
        raise

def get_template_code(scene):
    """
    根据场景获取模板代码
    :param scene: 场景类型
    :return: 模板代码
    """
    template_mapping = {
        SmsScene.REGISTER: settings.ALIYUN_SMS_TEMPLATE_CODE_REGISTER,
        SmsScene.LOGIN: settings.ALIYUN_SMS_TEMPLATE_CODE_LOGIN,
        SmsScene.RESET_PASSWORD: settings.ALIYUN_SMS_TEMPLATE_CODE_RESET_PASSWORD
    }
    return template_mapping.get(scene)

def send_sms(phone, code, scene=SmsScene.REGISTER):
    """
    发送短信验证码
    :param phone: 手机号
    :param code: 验证码
    :param scene: 场景，默认为注册
    :return: (bool, str) 发送结果和消息
    """
    try:
        client = get_sms_client()
        template_code = get_template_code(scene)
        
        if not template_code:
            logger.error(f"未找到场景 {scene} 对应的模板")
            return False, f"未找到场景 {scene} 对应的模板"
            
        # 记录请求参数
        logger.info(f"""
=== 短信发送请求参数 ===
手机号: {phone}
验证码: {code}
场景: {scene}
签名: {settings.ALIYUN_SMS_SIGN_NAME}
模板ID: {template_code}
====================
        """)
        
        # 构建请求
        request = dysmsapi_models.SendSmsRequest(
            phone_numbers=phone,
            sign_name=settings.ALIYUN_SMS_SIGN_NAME,
            template_code=template_code,
            template_param='{"code":"%s"}' % code
        )
        
        # 发送请求
        logger.info("正在发送短信...")
        response = client.send_sms(request)
        
        # 记录响应信息
        logger.info(f"""
=== 短信发送响应信息 ===
响应代码: {response.body.code}
响应消息: {response.body.message}
请求ID: {response.body.request_id}
====================
        """)
        
        success = response.body.code == "OK"
        if not success:
            error_message = response.body.message
            if "触发小时级流控" in error_message:
                return False, ResponseMessage.SMS_RATE_LIMIT
            logger.error(f"发送失败原因: {error_message}")
            return False, error_message
            
        return True, ResponseMessage.SMS_SEND_SUCCESS
        
    except Exception as e:
        logger.exception("短信发送异常")
        return False, str(e)