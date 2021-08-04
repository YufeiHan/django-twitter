from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from accounts.api.serializers import (
    UserSerializer,
    LoginSerializer,
    SignupSerializer
)
from django.contrib.auth import (
    login as django_login,
    logout as django_logout,
    authenticate as django_authenticate
)


# ModelViewSet has list/retrieve/put/patch/destroy
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


# our customized ViewSet can have its own actions
class AccountViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer

    @action(methods=['GET'], detail=False)
    def login_status(self, request):
        # 'ip': request.META['REMOTE_ADDR']
        data = {'has_logged_in': request.user.is_authenticated}
        if request.user.is_authenticated:
            data['user'] = UserSerializer(request.user).data
        return Response(data)

    @action(methods=['POST'], detail=False)
    def logout(self, request):
        django_logout(request)
        return Response({'success': True})

    @action(methods=['POST'], detail=False)
    def login(self, request):
        # get username and password from request
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Please check input.",
                "errors": serializer.errors,
            }, status=400)

        # validation is ok, log in
        # 这里也可以直接从request.data去取，但是专业一点是从validated_data去取
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = django_authenticate(username=username, password=password)

        if not user or user.is_anonymous:
            return Response({
                "success": False,
                "message": "Username and password does not match.",
            }, status=400)

        django_login(request, user)
        return Response({
            "success": True,
            "user": UserSerializer(instance=user).data,
            # "user": UserSerializer(user).data # instance= is optional
        })

    @action(methods=['POST'], detail=False)
    def signup(self, request):
        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Please check input.",
                "errors": serializer.errors,
            }, status=400)

        user = serializer.save()
        django_login(request, user)
        return Response({
            "success": True,
            "user": UserSerializer(instance=user).data,
        }, status=201)