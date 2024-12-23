from typing import Optional
import os
import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings

from users.views.base import ProtectedAPIView
from users.views.mixins import ResponseMixin, LoggerMixin
from users.serializers import UserProfileSerializer
from users.constants import ResponseCode, ResponseMessage

logger = logging.getLogger('users')

class UserProfileView(ProtectedAPIView, ResponseMixin):
    """
    用户资料管理
    
    get: 获取用户资料
    put: 更新用户资料
    """
    serializer_class = UserProfileSerializer
    
    def get_profile(self, request: Request):
        """获取用户资料"""
        try:
            return request.user.profile
        except Exception as e:
            logger.exception("获取用户资料失败")
            return None

    def get(self, request: Request) -> Response:
        """获取用户资料"""
        profile = self.get_profile(request)
        if not profile:
            return self.error_response(
                message="获取用户资料失败",
                code=ResponseCode.NOT_FOUND,
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.serializer_class(profile)
        return self.success_response(
            message="获取成功",
            data=serializer.data
        )
    
    def put(self, request: Request) -> Response:
        """更新用户资料"""
        profile = self.get_profile(request)
        if not profile:
            return self.error_response(
                message="获取用户资料失败",
                code=ResponseCode.NOT_FOUND,
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.serializer_class(
            profile,
            data=request.data,
            partial=True,
            context={'request': request}  # 添加 request 到上下文
        )
        
        if not serializer.is_valid():
            return self.error_response(
                message="数据验证失败",
                errors=serializer.errors
            )
            
        try:
            serializer.save()
            return self.success_response(
                message="更新成功",
                data=serializer.data
            )
        except Exception as e:
            logger.exception("更新用户资料失败")
            return self.error_response(
                message=ResponseMessage.SERVER_ERROR,
                code=ResponseCode.SERVER_ERROR,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AvatarUploadView(ProtectedAPIView, ResponseMixin, LoggerMixin):
    """
    头像上传管理
    
    post: 上传新头像
    """
    parser_classes = (MultiPartParser, FormParser)
    
    # 允许的文件类型
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    # 最大文件大小 (5MB)
    MAX_FILE_SIZE = 5 * 1024 * 1024

    def get_parsers(self):
        """
        添加对 DRF 界面的支持
        """
        if self.request.content_type == 'application/x-www-form-urlencoded':
            return [FormParser()]
        return [MultiPartParser()]

    def validate_avatar(self, avatar) -> Optional[str]:
        """
        验证头像文件
        :return: 错误信息，如果没有错误则返回 None
        """
        if not avatar:
            return "请选择要上传的头像"

        # 检查文件大小
        if avatar.size > self.MAX_FILE_SIZE:
            return f"头像文件大小不能超过 {self.MAX_FILE_SIZE // 1024 // 1024}MB"

        # 检查文件类型
        ext = avatar.name.split('.')[-1].lower()
        if ext not in self.ALLOWED_EXTENSIONS:
            return f"只支持 {', '.join(self.ALLOWED_EXTENSIONS)} 格式的图片"

        return None

    def delete_old_avatar(self, profile) -> None:
        """删除旧头像"""
        try:
            if profile.avatar and os.path.exists(profile.avatar.path):
                os.remove(profile.avatar.path)
        except Exception as e:
            self.log_error(f"删除旧头像失败: {str(e)}")

    def post(self, request: Request) -> Response:
        """上传头像"""
        avatar = request.FILES.get('avatar')
        
        # 验证头像文件
        error = self.validate_avatar(avatar)
        if error:
            return self.error_response(message=error)

        try:
            profile = request.user.profile
            
            # 删除旧头像
            self.delete_old_avatar(profile)
            
            # 保存新头像
            profile.avatar = avatar
            profile.save()

            # 构建头像完整URL
            avatar_url = request.build_absolute_uri(profile.avatar.url)
            
            return self.success_response(
                message="头像上传成功",
                data={'avatar': avatar_url}
            )

        except Exception as e:
            self.log_error(f"头像上传失败: {str(e)}")
            return self.error_response(
                message=ResponseMessage.SERVER_ERROR,
                code=ResponseCode.SERVER_ERROR,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )