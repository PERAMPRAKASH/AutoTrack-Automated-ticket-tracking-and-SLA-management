from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ticketing.serializers import OrganizationTokenSerializer, EmployeeTokenSerializer, ManagerTokenSerializer, \
    SupportAgentTokenSerializer


@api_view(['POST'])
def org_token_view(request):
    serializer = OrganizationTokenSerializer(data=request.data)

    if serializer.is_valid():
        return Response(serializer.validated_data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def employee_token_view(request):
    serializer = EmployeeTokenSerializer(data=request.data)

    if serializer.is_valid():
        return Response(serializer.validated_data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def manager_token_view(request):
    serializer = ManagerTokenSerializer(data=request.data)

    if serializer.is_valid():
        return Response(serializer.validated_data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def support_agent_token_view(request):
    serializer = SupportAgentTokenSerializer(data=request.data)

    if serializer.is_valid():
        return Response(serializer.validated_data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)