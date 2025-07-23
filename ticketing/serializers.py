from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from ticketing.models import Organization, Employee, Manager, SupportAgent


class OrganizationSerializer(serializers.Serializer):
    class Meta:
        model = Organization
        fields = ['company_name', 'email', 'password', 'contact_no', 'country']
        extra_kwargs = {'password': {'write_only': True}}


class OrganizationTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            org = Organization.objects.get(email=email)
        except Organization.DoesNotExist:
            raise serializers.ValidationError("Organization not found.")

        if not org.check_password(password):
            raise serializers.ValidationError("Wrong password.")

        if not org.is_active:
            raise serializers.ValidationError("Organization inactive.")

        refresh = RefreshToken()
        refresh['org_id'] = org.id
        refresh['org_email'] = org.email

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class EmployeeTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            employee = Employee.objects.get(email=email)
        except Employee.DoesNotExist:
            raise serializers.ValidationError("Employee not found.")

        if password != employee.password:
            raise serializers.ValidationError("Wrong password.")

        if not employee.is_active:
            raise serializers.ValidationError("Employee inactive.")

        refresh = RefreshToken()
        refresh['employee_id'] = employee.id
        refresh['employee_email'] = employee.email

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class ManagerTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            manager = Manager.objects.get(email=email)
        except Manager.DoesNotExist:
            raise serializers.ValidationError("Manager not found.")

        if password != manager.password:
            raise serializers.ValidationError("Wrong password.")

        if not Manager.is_active:
            raise serializers.ValidationError("Manager inactive.")

        refresh = RefreshToken()
        refresh['manager_id'] = manager.id
        refresh['manager_email'] = manager.email

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class SupportAgentTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            support_agent = SupportAgent.objects.get(email=email)
        except SupportAgent.DoesNotExist:
            raise serializers.ValidationError("Manager not found.")

        if password != support_agent.password:
            raise serializers.ValidationError("Wrong password.")

        if not SupportAgent.is_active:
            raise serializers.ValidationError("Manager inactive.")

        refresh = RefreshToken()
        refresh['support_agent_id'] = support_agent.id
        refresh['support_agent_email'] = support_agent.email

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }