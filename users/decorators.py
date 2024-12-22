from functools import wraps
from typing import Callable, Any
from rest_framework.response import Response
from rest_framework import status
from users.constants import ResponseCode, ResponseMessage

def handle_view_exceptions(view_func: Callable) -> Callable:
    """
    视图异常处理装饰器
    """
    @wraps(view_func)
    def wrapper(*args: Any, **kwargs: Any) -> Response:
        try:
            return view_func(*args, **kwargs)
        except Exception as e:
            # 获取 self (视图实例)
            view = args[0]
            
            # 记录错误日志
            if hasattr(view, 'log_error'):
                view.log_error(f"视图执行异常: {str(e)}")
            
            # 返回错误响应
            if hasattr(view, 'error_response'):
                return view.error_response(
                    message=ResponseMessage.SERVER_ERROR,
                    code=ResponseCode.SERVER_ERROR,
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # 如果视图没有 error_response 方法，返回普通 Response
            return Response(
                {
                    'code': ResponseCode.SERVER_ERROR.value,
                    'message': ResponseMessage.SERVER_ERROR
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    return wrapper