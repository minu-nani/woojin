import logging
import inspect
import json
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.views import redirect_to_login
from django.core.cache import cache
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.response import Response

from .utils import set_input_params
from .formatter import default_logging_formatter, api_logging_formatter

logger = logging.getLogger('jobseek.mixins')


class MappingViewSetMixin(object):
    serializer_action_map = {}
    permission_classes_map = {}

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.permission_classes_map.get(self.action, None):
            permission_classes = self.permission_classes_map[self.action]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.serializer_action_map.get(self.action, None):
            return self.serializer_action_map[self.action]
        return self.serializer_class


class ViewSetLoggingMixin:
    def set_input_log(self, input_params=None):
        function_name = inspect.stack()[2][3]
        json_dump_input_params = json.dumps(input_params, cls=DjangoJSONEncoder, ensure_ascii=False)
        logger.info(f'API input - class: {self.__class__}, function: {function_name}, input_params: {json_dump_input_params}',
                    extra=api_logging_formatter(channel='WEB', request=None, direction='SERVER',
                                                message_type='text', status='VA'))

    def set_output_log(self, response=None):
        function_name = inspect.stack()[2][3]
        json_dump_response = json.dumps(response, cls=DjangoJSONEncoder, ensure_ascii=False)
        logger.info(f'API output - class: {self.__class__}, function: {function_name}, response: {json_dump_response}',
                    extra=api_logging_formatter(channel='WEB', request=None, direction='SERVER',
                                                message_type='text', status='VA'))


class ListModelMixin(ViewSetLoggingMixin):
    def list(self, request, *args, **kwargs):
        input_params = set_input_params(request, **kwargs)
        self.set_input_log(input_params=input_params)

        serializer = self.get_serializer(data=input_params)
        serializer.is_valid(raise_exception=True)
        response = serializer.data

        self.set_output_log(response=response)
        return Response(data=response)

    def list_instance(self, queryset):
        self.set_input_log(input_params=None)

        serializer = self.get_serializer(queryset, many=True)
        response = serializer.data

        self.set_output_log(response=response)
        return Response(data=response)


class RetrieveModelMixin(ViewSetLoggingMixin):
    def retrieve(self, request, *args, **kwargs):
        input_params = set_input_params(request, **kwargs)
        self.set_input_log(input_params=input_params)

        serializer = self.get_serializer(data=input_params)
        serializer.is_valid(raise_exception=True)
        response = serializer.data

        self.set_output_log(response=response)
        return Response(data=response)

    def retrieve_instance(self, instance):
        self.set_input_log(input_params=None)

        serializer = self.get_serializer(instance)
        response = serializer.data

        self.set_output_log(response=response)
        return Response(data=response)


class CreateModelMixin(ViewSetLoggingMixin):
    def create(self, request, *args, **kwargs):
        input_params = set_input_params(request, **kwargs)
        self.set_input_log(input_params=input_params)

        serializer = self.get_serializer(data=input_params)
        serializer.is_valid(raise_exception=True)
        response = serializer.data

        self.set_output_log(response=response)
        return Response(data=response, status=201)

    def get_or_create(self, request, *args, **kwargs):
        input_params = set_input_params(request, **kwargs)
        self.set_input_log(input_params=input_params)

        serializer = self.get_serializer(data=input_params)
        serializer.is_valid(raise_exception=True)
        response = serializer.data

        self.set_output_log(response=response)
        if response.get('is_created', True):
            return Response(data=response, status=201)
        return Response(data=response, status=200)


class UpdateModelMixin(ViewSetLoggingMixin):
    def update(self, request, *args, **kwargs):
        input_params = set_input_params(request, **kwargs)
        self.set_input_log(input_params=input_params)

        serializer = self.get_serializer(data=input_params)
        serializer.is_valid(raise_exception=True)
        response = serializer.data

        self.set_output_log(response=response)
        return Response(data=response, status=200)


class DeleteModelMixin(ViewSetLoggingMixin):
    def delete(self, request, *args, **kwargs):
        input_params = set_input_params(request, **kwargs)
        self.set_input_log(input_params=input_params)

        serializer = self.get_serializer(data=input_params)
        serializer.is_valid(raise_exception=True)
        response = serializer.data

        self.set_output_log(response=response)
        return Response(data=response, status=200)