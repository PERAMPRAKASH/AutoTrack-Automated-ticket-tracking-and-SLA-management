from datetime import date

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ticketing.models import Department, SupportAgent, DepartmentOnCallSchedule
from common.decorators import organization_required


def get_oncall(organization):
    department = dict(Department.objects.filter(organization=organization, is_active=True).values_list('id', 'dept_name'))
    if not department:
        return Response({'status': 'error', 'message': 'No department registered with organization.'},
                        status=status.HTTP_404_NOT_FOUND)

    oncall = []
    data = []

    for dept_id, dept_name in department.items():
        support_agents = list(SupportAgent.objects.filter(organization=organization, manager__department_id=dept_id, is_active=True).order_by('name'))
        if not support_agents:
            return Response({'status': 'error', 'message': 'No support agent registered with department.'},
                            status=status.HTTP_404_NOT_FOUND)

        count = len(support_agents)

        oncall_schedule = DepartmentOnCallSchedule.objects.filter(organization=organization, department=dept_id, is_active=True).first()
        if not oncall_schedule:
            return Response({'status': 'error', 'message': 'No support agent is at oncall from this department.'},
                            status=status.HTTP_404_NOT_FOUND)

        start_date = oncall_schedule.start_date

        days_passed = (date.today() - start_date).days
        index = (days_passed // 2) % count

        support_agent_data = support_agents[index]
        oncall.append({"emp_code": support_agent_data.emp_code, support_agent_data.manager.department.dept_name: support_agent_data.name})
        data.append({"id": support_agent_data.id, "department_id": support_agent_data.manager.department_id, "department": support_agent_data.manager.department.dept_name})

    return oncall, data


@api_view(['GET'])
@organization_required
def get_oncall_each_level(request):
    organization = request.organization

    oncall, data = get_oncall(organization)

    return Response({'status': 'success', 'data': oncall}, status=status.HTTP_200_OK)
