from django.core.management.base import BaseCommand
from django.utils import timezone

from ticketing.models import CreateTicket, Manager, Priority


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        status_list = ['Open']

        tickets = CreateTicket.objects.filter(escalated_status=False, status__in=status_list)

        priority = dict(Priority.objects.values_list('id','duration'))

        tickets_not_escalated = []
        tickets_escalated = []

        for ticket in tickets:
            ticket_priority = ticket.priority_id

            duration = priority[ticket_priority]

            deadline = ticket.created_at + duration

            if timezone.now() > deadline:
                agent_manager = ticket.assign_to.manager
                if not agent_manager or not agent_manager.is_active:
                    tickets_not_escalated.append({'message': 'No manager found to escalate the ticket.',
                                                  'title': ticket.title,
                                                  'ticket_cut_by': ticket.employee.name,
                                                  'ticket_cut_to': ticket.assign_to.name,
                                                  'department': ticket.department.dept_name,
                                                  'organization': ticket.organization.company_name})
                    continue

                else:
                    escalate = ticket.assign_to.manager
                    ticket.escalated_to = escalate
                    ticket.escalated_status = True
                    ticket.save()
                    tickets_not_escalated.append({'message': 'Ticket escalated successfully.',
                                                  'title': ticket.title,
                                                  'ticket_cut_by': ticket.employee.name,
                                                  'ticket_cut_to': ticket.assign_to.name,
                                                  'department': ticket.department.dept_name,
                                                  'organization': ticket.organization.company_name})

        if tickets_not_escalated:
            for ticket in tickets_not_escalated:
                self.stdout.write(str(ticket))

        if tickets_escalated:
            for ticket in tickets_escalated:
                self.stdout.write(str(ticket))
