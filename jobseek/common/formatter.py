from django.conf import settings


def default_logging_formatter(channel="UNKNOWN",
                              user_key="UNKNOWN", direction="UNKNOWN",
                              message_type="UNKNOWN", status="VA"):
    log_params = {
        "channel": channel.upper(),
        "user_key": user_key,
        "direction": direction,
        "message_type": message_type.upper(),
        "status": status
    }
    return log_params


def api_logging_formatter(channel="UNKNOWN",
                          request=None, direction="UNKNOWN",
                          message_type="UNKNOWN", status="VA"):
    user_key = "UNKNOWN"

    if hasattr(settings, 'PROJECT_USER') and settings.PROJECT_USER == 'cassiere':
        user_key = 'cassiere'
    else:
        if request:
            user = request.user
            if user.username == '':
                user_key = 'AnonymousUser'
            elif hasattr(user, 'chatsession'):
                user_key = user.chatsession.user_key
            else:
                user_key = user.username
    log_params = {
        "channel": channel.upper(),
        "user_key": user_key,
        "direction": direction,
        "message_type": message_type.upper(),
        "status": status
    }
    return log_params