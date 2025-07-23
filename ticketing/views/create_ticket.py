from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework import status

from ticketing.authentication import EmployeeJWTAuthentication
from ticketing.models import Organization, CreateTicket, Priority
from common.decorators import employee_required, validate_keys
from ticketing.views.get_data import get_oncall


@api_view(['POST'])
@validate_keys(['title','description','priority','department'])
@authentication_classes([EmployeeJWTAuthentication])
@employee_required
def create_ticket(request):
    employee = request.user

    data = request.data
    domain = employee.email.split('@')[1]
    organization = Organization.objects.filter(domain=domain, is_active=True).first()
    if not organization:
        return Response({'status': 'error', 'message': 'Invalid email.'}, status=status.HTTP_404_NOT_FOUND)

    oncall, detail = get_oncall(organization)

    support_agent = {}

    for detail in detail:
        if detail['department'] == data['department']:
            support_agent.update(detail)
            break

    if not support_agent:
        return Response({'status': 'error', 'message': f'{data['department']} not exists.'}, status=status.HTTP_404_NOT_FOUND)

    priority = dict(Priority.objects.values_list('priority','id'))
    if data['priority'] not in priority:
        return Response({'status': 'error', 'message': 'Priority not found.', 'option': priority.keys()}, status=status.HTTP_404_NOT_FOUND)

    attachment = data.get('attachment')
    if not attachment:
        attachment = None

    CreateTicket.objects.create(organization=organization, title=data['title'], description=data['description'],
                                priority_id=priority[data['priority']], attachment=attachment, employee=employee,
                                department_id=support_agent['department_id'], assign_to_id=support_agent['id'],escalated_to=None)

    return Response({'status': 'success', 'message': 'Ticket created successfully'}, status=status.HTTP_200_OK)