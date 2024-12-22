from typing import Any, Dict, Optional, Type
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.pagination import PageNumberPagination
from django.db.models.query import QuerySet
from users.decorators import handle_view_exceptions
from users.constants import ResponseCode, ResponseMessage

class CustomPagination(PageNumberPagination):
    """自定义分页器"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class BaseAPIView(APIView):
    """
    基础API视图
    提供异常处理和通用响应方法
    """
    pagination_class = CustomPagination

    def get_paginator(self) -> PageNumberPagination:
        """获取分页器实例"""
        return self.pagination_class()

    def success_response(
        self, 
        message: str = ResponseMessage.SUCCESS, 
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
        response_data: Dict[str, Any] = {
            'code': ResponseCode.SUCCESS.value,
            'message': message
        }
        if data is not None:
            response_data['data'] = data
        return Response(response_data, status=status)

    def error_response(
        self, 
        message: str, 
        errors: Optional[Dict[str, Any]] = None, 
        code: ResponseCode = ResponseCode.BAD_REQUEST,
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
        response_data: Dict[str, Any] = {
            'code': code.value,
            'message': message
        }
        if errors:
            response_data['errors'] = errors
        return Response(response_data, status=status)

    def paginate_response(
        self, 
        queryset: QuerySet, 
        serializer_class: Type[Serializer], 
        request: Request,
        extra_data: Optional[Dict[str, Any]] = None
    ) -> Response:
        """
        分页响应
        :param queryset: 查询集
        :param serializer_class: 序列化器类
        :param request: 请求对象
        :param extra_data: 额外的响应数据
        :return: Response 对象
        """
        paginator = self.get_paginator()
        page = paginator.paginate_queryset(queryset, request)
        
        if page is not None:
            serializer = serializer_class(page, many=True)
            response_data = {
                'total': paginator.page.paginator.count,
                'items': serializer.data,
                'page': request.query_params.get('page', 1),
                'page_size': paginator.page_size
            }
            
            if extra_data:
                response_data.update(extra_data)
                
            return self.success_response(data=response_data)
            
        serializer = serializer_class(queryset, many=True)
        return self.success_response(data={'items': serializer.data})

class PublicAPIView(BaseAPIView):
    """
    公开API视图
    无需认证即可访问
    """
    permission_classes = [AllowAny]
    authentication_classes: list = []  # 无需认证

class ProtectedAPIView(BaseAPIView):
    """
    需要认证的API视图
    必须提供有效的认证令牌
    """
    permission_classes = [IsAuthenticated]