# from django.utils.deprecation import MiddlewareMixin
# from django.http import JsonResponse
# from django.urls import resolve
# from Client.models import GasStation  # Import the Station model

# class TenantMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         # Extract tenant from the logged-in user
#         if request.user.is_authenticated:
#             request.tenant = getattr(request.user, 'tenant', None)
#         else:
#             request.tenant = None

#         # Check the current path and skip station check for specific URLs
#         current_path = request.path_info

#         # Skip station check for Django admin or authentication-related URLs
#         if current_path.startswith('/admin/') or current_path in ['/auth/api/token/', '/auth/api/token/']:
#             return

#         # Extract station from the header
#         station_id = request.headers.get('X-Station-ID')
#         if not station_id:
#             return JsonResponse({'error': 'Station ID is required'}, status=400)

#         # Try to retrieve the station instance
#         try:
#             request.station = GasStation.objects.get(id=station_id)
#         except (ValueError, GasStation.DoesNotExist):
#             return JsonResponse({'error': 'Invalid Station ID'}, status=400)

# import threading
# from django.utils.deprecation import MiddlewareMixin
# from django.http import JsonResponse
# from django.db import IntegrityError
# # from Client.models import GasStation  # Import the Station model

# # Thread-local storage to store the current request
# _thread_locals = threading.local()

# def get_current_request():
#     return getattr(_thread_locals, 'request', None)

# class CurrentRequestMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         # Store the current request in thread-local storage
#         _thread_locals.request = request

#         # Extract tenant from the logged-in user
#         if request.user.is_authenticated:
#             request.tenant = getattr(request.user, 'tenant', None)
#         else:
#             request.tenant = None

#         # Skip station check for Django admin or authentication-related URLs
#         current_path = request.path_info
#         if current_path.startswith('/admin/') or current_path in ['/auth/api/token/', '/api/station/', '/auth/api/token/refresh/']:
#             return

#         # Extract station from the header
#         station_id = request.headers.get('X-Station-ID')
#         if not station_id:
#             return JsonResponse({'error': 'Station ID is required'}, status=400)

#         # Try to retrieve the station instance
#         try:
#             from Client.models import GasStation  # Import the Station model
#             request.station = GasStation.objects.get(id=station_id)
#             print(f"Middleware: Station found and set - {request.station}")
#         except (ValueError, GasStation.DoesNotExist):
#             return JsonResponse({'error': 'Invalid Station ID'}, status=400)


# class IntegrityErrorMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)
#         return response

#     def process_exception(self, request, exception):
#         if isinstance(exception, IntegrityError):
#             return JsonResponse({"error": "Database constraint violation. Possible duplicate entry."}, status=400)
#         return None
