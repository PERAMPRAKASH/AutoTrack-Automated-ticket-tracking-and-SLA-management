import csv
from datetime import date, timedelta
from io import StringIO

from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ticketing.models import Organization, Department, Employee, SupportAgent, DepartmentOnCallSchedule, Manager, \
    Priority
from common.decorators import validate_keys, organization_required


@api_view(['POST'])
@validate_keys(['email','password','company_name','contact_no','country'])
def register_info(request):
    data = request.data

    email = data.get('email')

    try:
        validate_email(email)
    except DjangoValidationError:
        raise ValidationError({'message': 'Invalid email format.'})

    org_domain = email.split('@')[1]
    get_domain_list = Organization.objects.values_list('domain', flat=True)

    if org_domain in get_domain_list:
        return Response({'message': 'Organization already registered.'}, status=status.HTTP_400_BAD_REQUEST)

    Organization.objects.create(company_name=data['company_name'], email=data['email'], password=make_password(data['password']),
                                domain=org_domain, contact_no=data['contact_no'], country=data['country'])

    return Response({'message': 'Registration successful.'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@organization_required
def upload_department_csv_file(request):
    organization = request.organization

    uploaded_file = request.FILES.get('file')

    with transaction.atomic():
        if not uploaded_file:
            return Response({'error': 'No file provided.'}, status=400)

        if not uploaded_file.name.endswith('.csv'):
            return Response({'error': 'File must end with .csv.'}, status=400)

        try:
            content = uploaded_file.read().decode('utf-8').strip()
            if not content:
                return JsonResponse({'status': 'error', 'message': 'CSV file is empty.'})
        except:
            return JsonResponse({'status': 'error', 'message': 'CSV file must be a valid UTF-8.'})

        csv_file = StringIO(content)
        reader = csv.reader(csv_file)

        header = next(reader)
        if 'Department' not in header:
            return JsonResponse({'status': 'error', 'message': 'Missing Required Header: Department.'})

        invalid_format = {}
        department_list = []

        for index, row in enumerate(reader, start=2):
            dept_name = row[0].strip() if row else ''
            if not dept_name or not isinstance(dept_name, str):
                invalid_format[index] = 'Department must be a non-empty string.'
                continue
            department_list.append(dept_name)

        if invalid_format:
            return JsonResponse({'status': 'error', 'message': invalid_format})

        existing_dept = Department.objects.filter(organization=organization).values_list('dept_name',flat=True)

        department = []
        for dept in department_list:
            if dept not in existing_dept:
                department.append(Department(organization=organization, dept_name=dept))

        Department.objects.bulk_create(department)

        department_ids = Department.objects.filter(organization=organization).values_list('id',flat=True)
        if not department_ids:
            return Response({'status': 'error', 'message': 'No department registered.'})

        oncall_schedule = []
        for id in department_ids:
            oncall_schedule.append(DepartmentOnCallSchedule(organization=organization,department_id=id,start_date=date.today()))

        DepartmentOnCallSchedule.objects.bulk_create(oncall_schedule)

        # Priority.objects.create(priority='Low', duration=timedelta(hours=48))
        # Priority.objects.create(priority='Medium', duration=timedelta(hours=24))
        # Priority.objects.create(priority='High', duration=timedelta(hours=4))

        return Response({'status': 'success', 'message': 'Departments registered successfully.'})


@api_view(['POST'])
@organization_required
def upload_employee_data_csv_file(request):
    organization = request.organization

    uploaded_file = request.FILES.get('file')

    with transaction.atomic():
        if not uploaded_file:
            return Response({'error': 'No file provided.'}, status=400)

        if not uploaded_file.name.endswith('.csv'):
            return Response({'error': 'File must end with .csv.'}, status=400)

        try:
            content = uploaded_file.read().decode('utf-8').strip()
            if not content:
                return JsonResponse({'status': 'error', 'message': 'CSV file is empty.'})
        except:
            return JsonResponse({'status': 'error', 'message': 'CSV file must be a valid UTF-8.'})

        csv_file = StringIO(content)
        reader = csv.reader(csv_file)

        header = next(reader)
        mandatory_headers = ['emp_code', 'name', 'email', 'password', 'contact_no', 'department', 'manager']

        for index, data in enumerate(header):
            mandatory_data = mandatory_headers[index]
            if data!=mandatory_data:

                return Response({'status': 'error', 'message': 'Mandatory fields are not present or headers is not in proper format.',
                                 'data_format': mandatory_headers},status=status.HTTP_400_BAD_REQUEST)

        rows= list(reader)

        org_domain = organization.domain
        incorrect_domain = {}
        for index, row in enumerate(rows, start=2):
            email = row[2].strip()
            domain = email.split('@')[1]
            if domain != org_domain:
                incorrect_domain[row[0].strip()] = f'Incorrect domain {domain}'
                continue

        if incorrect_domain:
            return Response({'status': 'error', 'message': incorrect_domain}, status=status.HTTP_400_BAD_REQUEST)

        department_dict = dict(Department.objects.filter(organization=organization).values_list('dept_name','id'))

        for index, row in enumerate(rows, start=2):
            if department_dict.get(row[5].strip()):
                if row[6].strip() == "":
                    manager = Manager()
                    manager.emp_code = row[0].strip()
                    manager.name = row[1].strip()
                    manager.email = row[2].strip()
                    manager.password = row[3].strip()
                    manager.contact_no = row[4].strip()
                    manager.organization = organization
                    manager.department_id = department_dict[row[5].strip()]
                    manager.save()

        manager_dict = dict(Manager.objects.filter(organization=organization, is_active=True).values_list('emp_code','id'))

        invalid_employees = {}
        for index, row in enumerate(rows, start=2):
            if department_dict.get(row[5].strip()):
                if row[6].strip():
                    department = manager_dict.get(row[6].strip())
                    if not department:
                        invalid_employees[row[0].strip()] = f'No manager in {department}.'
                        continue

        if invalid_employees:
            raise ValidationError({'status': 'error', 'message': invalid_employees})

        for index, row in enumerate(rows, start=2):
            if department_dict.get(row[5].strip()):
                if row[6].strip():
                    support_agent = SupportAgent()
                    support_agent.emp_code = row[0].strip()
                    support_agent.name = row[1].strip()
                    support_agent.email = row[2].strip()
                    support_agent.password = row[3].strip()
                    support_agent.contact_no = row[4].strip()
                    support_agent.organization = organization
                    support_agent.manager_id = manager_dict[row[6].strip()]
                    support_agent.save()

            employee = Employee()
            employee.emp_code = row[0].strip()
            employee.name = row[1].strip()
            employee.email = row[2].strip()
            employee.password = row[3].strip()
            employee.contact_no = row[4].strip()
            employee.organization = organization
            employee.save()

        return Response({'status': 'success', 'message': 'Employees registered successfully.'}, status=status.HTTP_201_CREATED)
