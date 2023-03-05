# import pytz
# from django.utils import timezone
#
#
# class TimezoneMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         try:
#             tzname = request.session.get('django_timezone')
#             timezone.activate(pytz.timezone(tzname))
#         except:
#             timezone.deactivate()
#         return self.get_response(request)
#
