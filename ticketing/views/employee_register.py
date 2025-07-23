from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ticketing.models import Employee
from common.decorators import validate_keys, organization_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


@api_view(['POST'])
@validate_keys(['name', 'email', 'password', 'contact_no'])
@organization_required
def employee_register(request):
    organization = request.organization

    data = request.data

    email = data.get('email')

    try:
        validate_email(email)
    except ValidationError:
        return Response({'message': 'Invalid email format.'}, status=status.HTTP_400_BAD_REQUEST)

    org_domain = organization.domain
    email_domain = email.split('@')[1]

    if org_domain != email_domain:
        return Response({'status': 'error', 'message': 'Incorrect Domain'}, status=status.HTTP_400_BAD_REQUEST)

    last_emp = Employee.objects.filter(organization=organization).last()

    employee = Employee()
    if last_emp:
        emp_code = last_emp.emp_code
        emp_num = emp_code.split('E')[1]

        emp_num = int(emp_num) + 1
        employee.emp_code = 'E' + str(emp_num)

    else:
        employee.emp_code = 'E1'

    employee.name = data['name']
    employee.email = data['email']
    employee.password = data['password']
    employee.contact_no = data['contact_no']
    employee.organization = organization
    employee.save()

    return Response({'status': 'success'}, status=status.HTTP_201_CREATED)