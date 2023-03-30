from rest_framework.permissions import BasePermission
from .utils import decodeJWT
from rest_framework.response import Response
from rest_framework.views import exception_handler


class IsAuthenticatedCustom(BasePermission):
    """_summary_

    Args:
        object (_type_): _description_ 
    """    
    
    def has_permission(self, request, _):
        try:
            auth_token = request.Meta.get("HTTP_AUTHORIZATION", None)
        except Exception as E:
            return False
        if not auth_token:
            return False
       
        user = decodeJWT(auth_token)
       
        if not user: 
            return False
       
        request.user = user
        return True
    
    
def custom_exception_handler(exc, content):
    response = exception_handler(exc, content)
    
    if response is not None:
        return response
    
    exc_list = str(exc).split("DETAIL:")
    return Response({"error": exc_list[-1]}, status=403)