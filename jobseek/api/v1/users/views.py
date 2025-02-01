import logging
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ModelViewSet

from jobseek.domain.user.models import User, UserProfile
from jobseek.domain.user.serializers import UserSerializer, UserProfileSerializer, UserProfileUpdateSerializer, \
    UserProfileCreateSerializer
from jobseek.common.mixins import MappingViewSetMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin

logger = logging.getLogger('jobseek.api.user')


class UserViewSet(MappingViewSetMixin, RetrieveModelMixin, ModelViewSet):
    permission_classes = [AllowAny, ]
    authentication_classes = []

    serializer_action_map = {
        'create': UserProfileCreateSerializer,
        'list': UserProfileSerializer,
    }

    def get_queryset(self):
        return UserProfile.objects.all()

    @swagger_auto_schema(responses={200: UserProfileSerializer})
    def create(self, request, *args, **kwargs):
        """
        유저 생성 API

        유저 회원가입을 진행합니다.
        """
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: UserProfileSerializer})
    def list(self, request, *args, **kwargs):
        """
        전체 고객 리스트 조회 API

        전체 고객 리스트를 조회합니다.
        """
        return super().list(request, *args, **kwargs)