import csv

from django.http import HttpResponse
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework import status

from ticketing.authentication import ManagerJWTAuthentication
from ticketing.models import Organization, Department, Employee, SupportAgent, Manager
from common.decorators import organization_required, manager_required


@api_view(['GET'])
@organization_required
def download_organization_all_employees(request):
    organization = request.organization

    all_employees = Employee.objects.filter(organization=organization, is_active=True)

    if not all_employees:
        return Response({'status': 'error', 'message': 'No employee found.'}, status=status.HTTP_404_NOT_FOUND)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="All Employees.csv"'

    writer = csv.writer(response)
    writer.writerow(['emp_code', 'name', 'email'])

    for employee in all_employees:
        writer.writerow([employee.emp_code, employee.name, employee.email])

    return response


@api_view(['GET'])
@organization_required
def download_support_agent(request):
    organization = request.organization

    all_employees = SupportAgent.objects.filter(organization=organization, is_active=True)

    if not all_employees:
        return Response({'status': 'error', 'message': 'No support agent found.'}, status=status.HTTP_404_NOT_FOUND)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Support Agent.csv"'

    writer = csv.writer(response)
    writer.writerow(['emp_code', 'name', 'email'])

    for employee in all_employees:
        writer.writerow([employee.emp_code, employee.name, employee.email])

    return response


@api_view(['GET'])
@organization_required
def download_manager(request):
    organization = request.organization

    manager = Manager.objects.filter(organization=organization, is_active=True)

    if not manager:
        return Response({'status': 'error', 'message': 'No manager found.'}, status=status.HTTP_404_NOT_FOUND)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Manager.csv"'

    writer = csv.writer(response)
    writer.writerow(['emp_code', 'name', 'email'])

    for manager in manager:
        if manager.department is not None:
            writer.writerow([manager.emp_code, manager.name, manager.email])

    return response

@api_view(['GET'])
@authentication_classes([ManagerJWTAuthentication])
@manager_required
def download_manager_employees(request):
    manager = request.manager

    organization = manager.organization

    if not manager:
        return Response({'status': 'error', 'message': 'Manager not found.'}, status=status.HTTP_404_NOT_FOUND)

    employees = SupportAgent.objects.filter(organization=organization, manager=manager, is_active=True)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Manager Employees.csv"'

    writer = csv.writer(response)
    writer.writerow(['emp_code', 'name', 'email'])

    for employee in employees:
        writer.writerow([employee.emp_code, employee.name, employee.email])

    return response
