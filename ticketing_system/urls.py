from django.contrib import admin
from django.urls import path, include
from ticketing.views import token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('ticketing.urls')),
    path('api/token/', token.org_token_view, name='token_obtain_pair'),
    path('api/employee_token/', token.employee_token_view, name='employee_token'),
    path('api/manager_token/', token.manager_token_view, name='manager_token'),
    path('api/support_agent_token/', token.support_agent_token_view, name='support_agent_token')
]
