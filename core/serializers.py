from rest_framework import serializers
from .models import CustomUser, Roles, UserActivities

class CreateUserSerializer(serializers.Serializer):
    """_summary_

    Args:
        serializers (_type_): _description_
    """    
    
    email = serializers.EmailField()
    fullname = serializers.CharField()
    role = serializers.ChoiceField(Roles)
    
    
class LoginSerializer(serializers.Serializer):
    """_summary_

    Args:
        serializers (_type_): _description_
    """        
        
    email = serializers.EmailField()
    password = serializers.CharField(required=False)
    is_new_user = serializers.BooleanField(default=False, required=False)
        
        

class UpdatePasswordSerializer(serializers.Serializer):
    """_summary_

    Args:
        serializers (_type_): _description_
    """   
    
    user_id = serializers.CharField()
    password = serializers.CharField()



class CustomUserSerializer(serializers.ModelSerializer):
    """_summary_

    Args:
        serializers (_type_): _description_
    """   
    
    class Meta:
        model = CustomUser
        exclude = ('password', )
     
     
class UserActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivities
        fields = ("__all__")