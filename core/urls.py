from django.urls import path, include
from.views import (
    CreateUserView, LoginView, UpdatePasswordView, MeView, 
    UserActivitiesView, UsersView
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

router.register('create-user', CreateUserView, 'create a new user')
router.register('login', LoginView, 'login user')
router.register('update-password', UpdatePasswordView, 'update user password')
router.register('me', MeView, 'me')
router.register('activities-log', UserActivitiesView, 'activities log')
router.register('users', UsersView, 'users')


urlpatterns = [
    path('', include(router.urls))
]
