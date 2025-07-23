from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework import status

from ticketing.authentication import SupportAgentJWTAuthentication, ManagerJWTAuthentication, EmployeeJWTAuthentication
from ticketing.models import CreateTicket
from common.decorators import employee_required, validate_keys, support_agent_required, manager_required


@api_view(['PATCH'])
@authentication_classes([SupportAgentJWTAuthentication])
@support_agent_required
@validate_keys(['status'])
def update_ticket_support_agent(request, pub_id):
    support_agent = request.support_agent
    data = request.data

    organization = support_agent.organization

    ticket = CreateTicket.objects.filter(organization=organization, pub_id=pub_id, assign_to=support_agent).first()
    if not ticket:
        return Response({'status': 'error', 'message': 'Incorrect ticket id.'}, status=status.HTTP_400_BAD_REQUEST)

    ticket_status = data['status']

    if ticket_status.lower() not in ['open', 'resolved', 'closed']:
        return Response({'status': 'error', 'message': 'Invalid status.'}, status=status.HTTP_400_BAD_REQUEST)

    if ticket.status.lower() == 'open':
        if ticket_status.lower() == 'resolved':
            ticket.status = ticket_status
            ticket.save()
        else:
            return Response({'status': 'error', 'message': 'Invalid status.'}, status=status.HTTP_400_BAD_REQUEST)

    else:
        ticket_status = ticket.status
        return Response({'message': f'Ticket is already {ticket_status}.'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'status': 'success', 'message': 'Status updated successfully.'}, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@authentication_classes([ManagerJWTAuthentication])
@manager_required
@validate_keys(['status'])
def update_ticket_manager(request, pub_id):
    manager = request.manager
    data = request.data

    organization = manager.organization

    ticket = CreateTicket.objects.filter(organization=organization, pub_id=pub_id, assign_to__manager=manager).first()
    if not ticket:
        return Response({'status': 'error', 'message': 'Incorrect ticket id.'}, status=status.HTTP_400_BAD_REQUEST)

    ticket_status = data['status']

    if ticket_status.lower() not in ['open', 'resolved', 'closed']:
        return Response({'status': 'error', 'message': 'Invalid status.'}, status=status.HTTP_400_BAD_REQUEST)

    if ticket.status.lower() == 'open':
        if ticket_status.lower() == 'resolved':
            ticket.status = ticket_status
            ticket.save()
        else:
            return Response({'status': 'error', 'message': 'Invalid status.'}, status=status.HTTP_400_BAD_REQUEST)

    else:
        ticket_status = ticket.status
        return Response({'message': f'Ticket is already {ticket_status}.'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'status': 'success', 'message': 'Status updated successfully.'}, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@authentication_classes([EmployeeJWTAuthentication])
@employee_required
@validate_keys(['status'])
def update_ticket_employee(request, pub_id):
    employee = request.employee
    data = request.data

    organization = employee.organization

    ticket = CreateTicket.objects.filter(organization=organization, pub_id=pub_id, employee=employee).first()
    if not ticket:
        return Response({'status': 'error', 'message': 'Incorrect ticket id.'}, status=status.HTTP_400_BAD_REQUEST)

    ticket_status = data['status']

    if ticket_status.lower() not in ['open', 'resolved', 'closed']:
        return Response({'status': 'error', 'message': 'Invalid status.'}, status=status.HTTP_400_BAD_REQUEST)

    if ticket.status.lower() == 'resolved':
        if ticket_status.lower() == 'closed':
            ticket.status = ticket_status
            ticket.save()
        else:
            return Response({'status': 'error', 'message': 'Invalid status.'}, status=status.HTTP_400_BAD_REQUEST)

    else:
        ticket_status = ticket.status
        return Response({'message': f'Ticket is {ticket_status}.'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'status': 'success', 'message': 'Status updated successfully.'}, status=status.HTTP_200_OK)

