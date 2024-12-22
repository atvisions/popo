import random
import string
import json
import logging
from typing import Optional
from django.conf import settings
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

logger = logging.getLogger('users')

def generate_code(length: int = 6) -> str:
    """
    生成数字验证码
    :param length: 验证码长度，默认6位
    :return: 数字验证码字符串
    """
    return ''.join(random.choices(string.digits, k=length))

def send_sms(phone: str, code: str, scene: str) -> bool:
    """
    发送短信
    :param phone: 手机号
    :param code: 验证码
    :param scene: 场景
    :return: 是否发送成功
    """
    try:
        # 初始化 AcsClient
        client = AcsClient(
            settings.ALIYUN['ACCESS_KEY_ID'],
            settings.ALIYUN['ACCESS_KEY_SECRET'],
            'cn-hangzhou'
        )

        # 组装请求对象
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https')
        request.set_version('2017-05-25')
        request.set_action_name('SendSms')

        # 设置发送参数
        request.add_query_param('PhoneNumbers', phone)
        request.add_query_param('SignName', settings.ALIYUN['SMS_SIGN_NAME'])
        request.add_query_param('TemplateCode', settings.ALIYUN['SMS_TEMPLATES'][scene])
        request.add_query_param('TemplateParam', json.dumps({'code': code}))

        # 发送请求
        response = client.do_action_with_exception(request)
        result = json.loads(response)

        # 检查发送结果
        success = result.get('Code') == 'OK'
        if not success:
            logger.error(f"短信发送失败: {result}")
            return False

        logger.info(f"短信发送成功 -> 手机号: {phone}, 场景: {scene}")
        return True

    except Exception as e:
        logger.exception(f"发送短信异常: {str(e)}")
        return False

# 显式导出函数
__all__ = ['generate_code', 'send_sms']