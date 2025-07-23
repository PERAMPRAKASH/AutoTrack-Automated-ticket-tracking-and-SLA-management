from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from ticketing.models import Organization, Employee, Manager, SupportAgent


class OrganizationJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        org_id = validated_token.get("org_id")

        if not org_id:
            raise AuthenticationFailed("Token missing org_id", code="token_not_valid")

        try:
            organization = Organization.objects.get(id=org_id)
        except Organization.DoesNotExist:
            raise AuthenticationFailed("Organization not found", code="token_not_valid")

        return organization


class EmployeeJWTAuthentication(JWTAuthentication):
    def get_user(self, validate_token):
        employee_id = validate_token.get("employee_id")

        if not employee_id:
            raise AuthenticationFailed("Token missing employee_id", code="token_not_valid")

        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            raise AuthenticationFailed("Employee not found", code="token_not_valid")

        return employee

class ManagerJWTAuthentication(JWTAuthentication):
    def get_user(self, validate_token):
        manager_id = validate_token.get("manager_id")

        if not manager_id:
            raise AuthenticationFailed("Token missing manager_id", code="token_not_valid")

        try:
            manager = Manager.objects.get(id=manager_id)
        except Manager.DoesNotExist:
            raise AuthenticationFailed("Manager not found", code="token_not_valid")

        return manager

class SupportAgentJWTAuthentication(JWTAuthentication):
    def get_user(self, validate_token):
        support_agent_id = validate_token.get("support_agent_id")

        if not support_agent_id:
            raise AuthenticationFailed("Token missing support_agent_id", code="token_not_valid")

        try:
            support_agent = SupportAgent.objects.get(id=support_agent_id)
        except SupportAgent.DoesNotExist:
            raise AuthenticationFailed("Manager not found", code="token_not_valid")

        return support_agent
