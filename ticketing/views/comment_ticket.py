from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework import status

from ticketing.authentication import SupportAgentJWTAuthentication, ManagerJWTAuthentication, EmployeeJWTAuthentication
from ticketing.models import CreateTicket, Comment
from common.decorators import employee_required, validate_keys, support_agent_required, manager_required


@api_view(['POST'])
@authentication_classes([SupportAgentJWTAuthentication])
@support_agent_required
@validate_keys(['comment'])
def comment_ticket_support_agent(request, pub_id):
    support_agent = request.support_agent
    data = request.data

    organization = support_agent.organization

    ticket = CreateTicket.objects.filter(organization=organization, pub_id=pub_id, assign_to=support_agent).first()
    if not ticket:
        return Response({'status': 'error', 'message': 'Incorrect ticket id.'}, status=status.HTTP_400_BAD_REQUEST)

    comment = data['comment']
    order = Comment.objects.filter(organization=organization, ticket=ticket).order_by('order').values_list('order', flat=True)
    value = int(1)
    if order:
        value = int(order.last()) + int(1)

    Comment.objects.create(organization=organization, comment=comment, ticket=ticket, order=value, support_agent=support_agent)

    return Response({'status': 'success', 'message': 'Comment successful.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([ManagerJWTAuthentication])
@manager_required
@validate_keys(['comment'])
def comment_ticket_manager(request, pub_id):
    manager = request.manager
    data = request.data

    organization = manager.organization

    ticket = CreateTicket.objects.filter(organization=organization, pub_id=pub_id, assign_to__manager=manager).first()
    if not ticket:
        return Response({'status': 'error', 'message': 'Incorrect ticket id.'}, status=status.HTTP_400_BAD_REQUEST)

    comment = data['comment']
    order = Comment.objects.filter(organization=organization, ticket=ticket).order_by('order').values_list('order',flat=True)
    value = int(1)
    if order:
        value = int(order.last()) + int(1)

    Comment.objects.create(organization=organization, comment=comment, ticket=ticket, order=value, manager=manager)

    return Response({'status': 'success', 'message': 'Comment successful.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([EmployeeJWTAuthentication])
@employee_required
@validate_keys(['comment'])
def comment_ticket_employee(request, pub_id):
    employee = request.employee
    data = request.data

    organization = employee.organization

    ticket = CreateTicket.objects.filter(organization=organization, pub_id=pub_id, employee=employee).first()
    if not ticket:
        return Response({'status': 'error', 'message': 'Incorrect ticket id.'}, status=status.HTTP_400_BAD_REQUEST)

    comment = data['comment']
    order = Comment.objects.filter(organization=organization, ticket=ticket).order_by('order').values_list('order',flat=True)
    value = int(1)
    if order:
        value = int(order.last()) + int(1)

    Comment.objects.create(organization=organization, comment=comment, ticket=ticket, order=value, employee=employee)

    return Response({'status': 'success', 'message': 'Comment successful.'}, status=status.HTTP_200_OK)
