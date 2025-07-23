from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework import status

from ticketing.authentication import SupportAgentJWTAuthentication, ManagerJWTAuthentication, EmployeeJWTAuthentication
from ticketing.models import CreateTicket, Comment
from common.decorators import employee_required, validate_keys, support_agent_required, organization_required, \
    manager_required


def get_ticket_info(ticket, organization):
    all_ticket = []

    for ticket in ticket:
        comment = {}
        ticket_comment = Comment.objects.filter(organization=organization, ticket=ticket).order_by('order')
        if ticket_comment:
            for ticket_comment in ticket_comment:
                key = None
                if ticket_comment.support_agent:
                    key = 'support_agent'
                elif ticket_comment.manager:
                    key = 'manager'
                elif ticket_comment.employee:
                    key = 'employee'
                comment[key + f'(Comment {ticket_comment.order})'] = ticket_comment.comment

        escalate = "null"
        if ticket.escalated_to:
            escalate = ticket.escalated_to.email

        all_ticket.append({'pub_id':ticket.pub_id,
                           'title': ticket.title,
                           'status': ticket.status,
                           'description': ticket.description,
                           'priority': ticket.priority.priority,
                           'created_by': ticket.employee.email,
                           'support_agent': ticket.assign_to.email,
                           'manager': ticket.assign_to.manager.email,
                           'department': ticket.department.dept_name,
                           'escalated_to': escalate,
                           'comment': comment})

    return all_ticket


@api_view(['GET'])
@organization_required
def get_all_tickets(request):
    organization = request.organization

    ticket = CreateTicket.objects.filter(organization=organization)
    if not ticket:
        return Response({'status': 'error', 'message': 'No ticket created.'}, status=status.HTTP_400_BAD_REQUEST)

    all_ticket = get_ticket_info(ticket, organization)

    return Response({'status': 'success', 'tickets': all_ticket})


@api_view(['GET'])
@authentication_classes([ManagerJWTAuthentication])
@manager_required
def get_team_tickets(request):
    manager = request.manager

    organization = manager.organization

    if not manager:
        return Response({'status': 'error', 'message': 'Manager not found.'}, status=status.HTTP_404_NOT_FOUND)

    ticket = CreateTicket.objects.filter(organization=organization, assign_to__manager=manager)
    if not ticket:
        return Response({'status': 'error', 'message': 'No ticket created.'}, status=status.HTTP_400_BAD_REQUEST)

    all_ticket = get_ticket_info(ticket, organization)

    return Response({'status': 'success', 'tickets': all_ticket})


@api_view(['GET'])
@authentication_classes([SupportAgentJWTAuthentication])
@support_agent_required
def get_support_agent_tickets(request):
    support_agent = request.support_agent

    organization = support_agent.organization

    if not support_agent:
        return Response({'status': 'error', 'message': 'Support agent not found.'}, status=status.HTTP_404_NOT_FOUND)

    ticket = CreateTicket.objects.filter(organization=organization, assign_to=support_agent)
    if not ticket:
        return Response({'status': 'error', 'message': 'No ticket created.'}, status=status.HTTP_400_BAD_REQUEST)

    all_ticket = get_ticket_info(ticket, organization)

    return Response({'status': 'success', 'tickets': all_ticket})


@api_view(['GET'])
@authentication_classes([EmployeeJWTAuthentication])
@employee_required
def get_employee_tickets(request):
    employee = request.employee

    organization = employee.organization

    if not employee:
        return Response({'status': 'error', 'message': 'Employee not found.'}, status=status.HTTP_404_NOT_FOUND)

    ticket = CreateTicket.objects.filter(organization=organization, employee=employee)

    if not ticket:
        return Response({'status': 'error', 'message': 'No ticket created.'}, status=status.HTTP_400_BAD_REQUEST)

    all_ticket = get_ticket_info(ticket, organization)

    return Response({'status': 'success', 'tickets': all_ticket})
