from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)

Roles = (('admin', 'admin'), ('creator', 'creator'), ('sale', 'sale'))


class CustomUserManager(BaseUserManager):
    """to setup a custom user model that inherits from the base user manager, this makes the user model to not setup the password at the point of registering

    Args:
        BaseUserManager (class): to create regular users, and to create superusers
    """     
    
    def create_superuser(self,email, password, **kwargs):
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_active', True)
        
        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must set is_staff = True')
        
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must set is_superuser = True')
        
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user
    
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Create a new Custom User

    Args:
        AbstractBaseUser (class): Base class User model for creating custom users
        PermissionsMixin (mixin: ability to assign permissions to custom users
        """         
        
    fullname = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True, blank=False)
    role = models.CharField(max_length=8, choices=Roles)
    created_at = models.DateTimeField(auto_now_add=True)        
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)       
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True)
        
    USERNAME_FIELD = 'email'
    objects = CustomUserManager()
    
    def __str__(self) -> str:
        return self.email
    
    
    class Meta:
        ordering = ('created_at',)
        
        
class UserActivities(models.Model):
    """_summary_

    Args:
        models (_type_): _description_
    """    
    
    user = models.ForeignKey(
        CustomUser, related_name="user_activities", null=True, on_delete=models.SET_NULL
    )
    email = models.EmailField()
    fullname = models.CharField(max_length=255)
    action = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-created_at', )
        
        
    def __str__(self):
        return f"{self.fullname} {self.action} on {self.created_at.strftime('%Y-%m-%d %H:%M')}"