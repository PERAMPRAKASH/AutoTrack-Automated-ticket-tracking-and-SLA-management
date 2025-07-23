from functools import wraps
from rest_framework.response import Response
from rest_framework import status

from ticketing.models import Organization, Employee, Manager, SupportAgent


def validate_keys(required_keys):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            for key in required_keys:
                if key not in request.data:
                    return Response({'message': f'{key} is missing'}, status=status.HTTP_400_BAD_REQUEST)
                if request.data.get(key) in [None, '', (), {}, []]:
                    return Response({'message': f'{key} value is missing'}, status=status.HTTP_400_BAD_REQUEST)
            return func(request, *args, **kwargs)
        return wrapper
    return decorator

def organization_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not isinstance(request.user, Organization):
            return Response({'error': 'Authentication failed. Expected organization.'}, status=401)
        request.organization = request.user

        return view_func(request, *args, **kwargs)
    return wrapper

def employee_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not isinstance(request.user, Employee):
            return Response({'error': 'Authentication failed. Expected employee.'}, status=401)
        request.employee = request.user
        return view_func(request, *args, **kwargs)
    return wrapper

def manager_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not isinstance(request.user, Manager):
            return Response({'error': 'Authentication failed. Expected manager.'}, status=401)
        request.manager = request.user
        return view_func(request, *args, **kwargs)
    return wrapper

def support_agent_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not isinstance(request.user, SupportAgent):
            return Response({'error': 'Authentication failed. Expected support agent.'}, status=401)
        request.support_agent = request.user
        return view_func(request, *args, **kwargs)
    return wrapper
