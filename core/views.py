from rest_framework.viewsets import ModelViewSet
from .serializers import (
    CreateUserSerializer,CustomUser, LoginSerializer, UpdatePasswordSerializer, 
    CustomUserSerializer, UserActivities, UserActivitiesSerializer
    )
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from datetime import datetime
from inventory_api.utils import get_access_token
from inventory_api.custom_methods import IsAuthenticatedCustom

def add_user_activity(user, activity):
    UserActivities.objects.create(
        user_id = user.id,
        email = user.email,
        fullname = user.fullname,
        activity = activity
    )


class CreateUserView(ModelViewSet):
    """_summary_

    Args:
        ModelViewSet (_type_): _description_
    """    

    http_method_names = ['post']
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (IsAuthenticatedCustom, )
    
    def create(self, request):
        """_summary_

        Args:
            request (_type_): _description_
        """        
        valid_request = self.serializer_class(data=request.data)
        valid_request.is_valid(raise_exception=True)
        
        CustomUser.objects.create(**valid_request.validated_data)
        
        add_user_activity(request.user, "added_new_user")
        
        return Response(
            {'success':'User created successfully'}, 
            status=status.HTTP_201_CREATED
            )
        
        
class LoginView(ModelViewSet):
    http_method_names = ['POST']
    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializer
    
    def create(self, request):
        """_summary_

        Args:
            request (_type_): _description_
        """        
        
        valid_request = self.serializer_class(data=request.data)
        valid_request.is_valid(raise_exception=True)
        
        new_user = valid_request.validated_data['is_new_user']
        
        if new_user:
            user = CustomUser.objects.filter(
                email= valid_request.validated_data['email'],
            )
            
            if user:
                user = user[0]
                
                if not user.password:
                    return Response({'user_id': user.id})
                
                raise Exception('User has a password already')
            
            raise Exception('Email doesn\'t exist')
        
        
        user = authenticate(
            username = valid_request.validated_data['email'],
            password = valid_request.validated_data.get('password', None)
        )
        
        if not user:
            return Response(
                {'error': 'Invalid email or Password'}, 
                status=status.HTTP_400_BAD_REQUEST
                )
            
        access = get_access_token({'user_id': user.id}, 1)
        user.last_login = datetime.now()
        
        user.save()
        
        add_user_activity(user, "user is now logged in")
         
        return Response({'access' :access })
        
        
class UpdatePasswordView(ModelViewSet):
    """_summary_

    Args:
        ModelViewSet (_type_): _description_
    """    
    
    serializer_class = UpdatePasswordSerializer
    http_method_names = ['POST']
    queryset = CustomUser.objects.all()
    
    def create(self, request, **kwargs):
        valid_request = self.serializer_class(data=request.data)
        valid_request.is_valid(raise_exception=True)
        
        user = CustomUser.objects.filter(id = valid_request.validated_data.get('user_id'))
        
        if not user:
            raise Exception('User not found')
        
        user = user[0]
        
        user.set_password(valid_request.validated_data.get('password'))
        user.save()
        
        add_user_activity(user, "updated password")
         
        return Response({'success': 'User Password was successfully updated'})
    
    
class MeView(ModelViewSet):
    """_summary_

    Args:
        ModelViewSet (_type_): _description_
    """    
    
    serializer_class = CustomUserSerializer
    http_method_names = ['GET']
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticatedCustom, )
    
    def list(self, request):
        data = self.serializer_class(request.user).data
        return Response(data)
    
    
class UserActivitiesView(ModelViewSet):
    serializer_class = UserActivitiesSerializer
    http_method_names = ["GET"]
    queryset = UserActivities.objects.all()
    permission_classes = (IsAuthenticatedCustom, )
    
    
class UsersView(ModelViewSet):
    serializer_class = CustomUserSerializer
    http_method_names = ["GET"]
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticatedCustom, )
    
    def list(self,request):
        users = self.queryset().filter(is_superuser=False)
        data = self.serializer_class(users, many=True).data
        return Response(data)