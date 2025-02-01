import logging
import json
from django.http.request import QueryDict
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse as django_reverse
from rest_framework.exceptions import ValidationError
from django.db import models
from datetime import datetime, timedelta, timezone, date
from pytz import timezone

from jobseek.common.formatter import default_logging_formatter

KST = timezone('Asia/Seoul')
logger = logging.getLogger('jobseek.utils')

def valid_input_parameter(serializer_class, **kwargs):
    serializer = serializer_class(data=kwargs)
    try:
        serializer.is_valid(raise_exception=True)
    except ValueError as e:
        error_text = e.args
        logger.error(msg='Invalid API input : %s' % error_text, extra=default_logging_formatter(
            channel='API_VIEW', user_key="NONE", direction='API_INPUT_VALIDATION', message_type='text', status='ERR'))
        raise e
    except ValidationError as e:
        error_text = e.detail
        logger.error(msg='Invalid API input : %s' % error_text, extra=default_logging_formatter(
            channel='API_VIEW', user_key="NONE", direction='API_INPUT_VALIDATION', message_type='text', status='ERR'))
        raise e

    json_dump_data = json.dumps(serializer.validated_data, cls=DjangoJSONEncoder, ensure_ascii=False)
    logger.info(msg='validated API input : %s' % json_dump_data, extra=default_logging_formatter(
        channel='API_VIEW', user_key="NONE", direction='API_INPUT_VALIDATION', message_type='text', status='VA'))
    return serializer.validated_data


def response_formatter(data, status=None):
    response = {'data': data}
    if status:
        response['status'] = status
    return response


def query_dict_to_dict(data):
    if type(data) == QueryDict:
        return data.dict()
    return data


def set_input_params(request, **kwargs):
    input_params = kwargs
    input_params.update(request.data)
    input_params.update(query_dict_to_dict(request.query_params))
    return input_params


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_user_agent(request):
    return request.META['HTTP_USER_AGENT']


def set_session_data(request):
    user_agent = get_user_agent(request)
    client_ip = get_client_ip(request)
    request.session['user_agent'] = user_agent
    request.session['client_ip'] = client_ip
    return


def reverse(viewname, urlconf=None, args=None, kwargs=None, current_app=None, query_kwargs=None):
    if query_kwargs:
        return '%s?%s' % (django_reverse(viewname, urlconf, args, kwargs, current_app), \
                        '&'.join(['%s=%s' % (k,v) for k,v in query_kwargs.items()]))
    else:
        return django_reverse(viewname, urlconf, args, kwargs, current_app)


def json_dumps_with_ascii(json_data):
    return json.dumps(json_data, cls=DjangoJSONEncoder, ensure_ascii=False)


def bulk_create_or_update(model_class, objs, match_field_names, update_field_names=None, exclude_field_names=None):
    def _get_filter_query(objs):
        return models.Q(
            *(
                models.Q(**{match_field.name: getattr(obj, match_field.name) for match_field in match_fields}) for obj in objs
            ),
            _connector=models.Q.OR,
        )

    def _get_match_values_by_obj(obj):
        ret = list()
        for match_field in match_fields:
            value = match_field.value_from_object(obj)
            if type(value) == datetime:
                value = value.date()

            ret.append(value)

        return tuple(ret)

    if model_class is None:
        raise ValueError()

    if update_field_names is None and exclude_field_names is None:
        raise ValueError()

    if len(objs) == 0:
        return 0, 0

    if exclude_field_names is not None:
        update_field_names = [entry.name for entry in model_class._meta.get_fields() if entry.name not in exclude_field_names]

    match_fields = [model_class._meta.get_field(name) for name in match_field_names]
    update_objs = model_class.objects.filter(_get_filter_query(objs))
    obj_map = {_get_match_values_by_obj(obj): obj for obj in objs}

    for entry in update_objs:
        obj = obj_map[_get_match_values_by_obj(entry)]
        for update_field in update_field_names:
            setattr(entry, update_field, getattr(obj, update_field))

        del obj_map[_get_match_values_by_obj(entry)]

    created_objs = []
    for obj in obj_map.values():
        created_objs.append(obj)

    model_class.objects.bulk_update(update_objs, update_field_names)
    model_class.objects.bulk_create(created_objs)

    return len(created_objs), len(update_objs)

