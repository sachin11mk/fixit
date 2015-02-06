# -*- coding: utf-8 -*-
from social_auth.middleware import SocialAuthExceptionMiddleware
from social_auth.exceptions import AuthFailed
from django.contrib import messages

class CustomSocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def get_message(self, request, exception):
        msg = None
        if (isinstance(exception, AuthFailed) and
            exception.message == u"User not allowed"):
            msg =   u"Not in whitelist"
        else:
            msg =   u"Some other problem"
        messages.add_message(request, messages.ERROR, msg)
