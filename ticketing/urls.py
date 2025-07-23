from django.urls import path
from ticketing.views import register, employee_register, download_data, get_data, create_ticket, get_ticket, update_ticket, comment_ticket

urlpatterns = [
    path('register/', register.register_info, name='register'),
    path('upload_department_csv_file/', register.upload_department_csv_file, name='upload_department_csv_file'),
    path('upload_employee_data_csv_file/', register.upload_employee_data_csv_file, name='upload_employee_data_csv_file'),

    path('employee_register/', employee_register.employee_register, name='employee_register'),

    path('download_organization_all_employees/', download_data.download_organization_all_employees, name='download_all_organization_employees'),
    path('download_support_agent/', download_data.download_support_agent, name='download_support_agent'),
    path('download_manager/', download_data.download_manager, name='download_manager'),
    path('download_manager_employees/', download_data.download_manager_employees, name='download_manager_employees'),

    path('get_oncall_each_level/', get_data.get_oncall_each_level, name='get_oncall_each_level'),

    path('create_ticket/', create_ticket.create_ticket, name='create_ticket'),

    path('get_all_tickets/', get_ticket.get_all_tickets, name='get_all_tickets'),
    path('get_team_tickets/', get_ticket.get_team_tickets, name='get_team_tickets'),
    path('get_support_agent_tickets/', get_ticket.get_support_agent_tickets, name='get_support_agent_tickets'),
    path('get_employee_tickets/', get_ticket.get_employee_tickets, name='get_employee_tickets'),

    path('update_ticket_support_agent/<str:pub_id>/', update_ticket.update_ticket_support_agent, name='update_ticket_support_agent'),
    path('update_ticket_manager/<str:pub_id>/', update_ticket.update_ticket_manager, name='update_ticket_manager'),
    path('update_ticket_employee/<str:pub_id>/', update_ticket.update_ticket_employee, name='update_ticket_employee'),

    path('comment_ticket_support_agent/<str:pub_id>/', comment_ticket.comment_ticket_support_agent, name='comment_ticket_support_agent'),
    path('comment_ticket_manager/<str:pub_id>/', comment_ticket.comment_ticket_manager, name='comment_ticket_manager'),
    path('comment_ticket_employee/<str:pub_id>/', comment_ticket.comment_ticket_employee, name='comment_ticket_employee'),
]