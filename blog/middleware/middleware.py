import logging
from django.http import HttpResponseServerError, HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.core.cache import cache
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import gettext_lazy as _
from blog.views import Magazines
from PIL import Image
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)


# class MyMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         print("Middleware processing request")
#         response = self.get_response(request)
#         print("Middleware processing response")
#         return response


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return redirect('/en/admin/login/?next=/en/admin/')
        response = self.get_response(request)
        return response


# class HandleMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         response = self.get_response(request)
#         return response
#
#     def process_exception(self, request, exception):
#         return HttpResponse("Custom Error")


# class ErrorHandlingMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         try:
#             response = self.get_response(request)
#             return response
#         except Exception as error:
#             return HttpResponseServerError("An error occurred in server: {}".format(error))

# class LogMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         response = self.get_response(request)
#         logging.basicConfig(level=logging.INFO)
#         logger.info("{} {} {} khaled".format(request.method, request.path, response.status_code))
# logging.basicConfig(level=logging.DEBUG)
# logger.debug('This is a debug message')
# logger.info('This is an info message')
# logger.warning('This is a warning message')
# logger.error('This is an error message')
# logger.critical('This is a critical message')
# return response

# class CacheMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
# def __call__(self, request):
#     key = 'blog:{}:{}'.format(request.method, request.path)
#     response = cache.get(key)
#     if response is not None:
#         return response
#     response = self.get_response(request)
# Cache the response for future requests
# cache.set(key, response)
# return response

# class ExtraDataMiddleware(MiddlewareMixin):
#     def process_view(self, request, view_func, view_args, view_kwargs):
#         if isinstance(view_func, Magazines.as_view().__class__):
#             extra_data = {'test': _('Middleware testing')}
#             request.extra_data = extra_data

# class CustomDataMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         response = self.get_response(request)
#         return response
#
#     def process_template_response(self, request, response, view=MyTestView.as_view().__class__):
#         response.context_data['my_data'] = 'Hello, World!'
#         return response


# class StreamingMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#     def __call__(self, request):
#         response = self.get_response(request)
#         if isinstance(response, StreamingHttpResponse):
#             def stream_chunks():
#                 total_data = 0
#                 for chunk in response.streaming_content:
#                     total_data += len(chunk)
#                     logging.basicConfig(level=logging.INFO)
#                     logger.info("Streaming response: %d bytes", total_data)
#                     yield chunk
#             return StreamingHttpResponse(stream_chunks(), content_type=response['Content-Type'])
#         return response
