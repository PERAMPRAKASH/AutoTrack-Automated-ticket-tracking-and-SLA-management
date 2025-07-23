from django.db import models
from common.common import generate_pub_id
from django.contrib.auth.hashers import make_password, check_password

class Organization(models.Model):
    pub_id = models.CharField(max_length=8, unique=True, default=generate_pub_id, editable=False)
    company_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    domain = models.CharField(max_length=100)
    password = models.CharField(max_length=200)
    contact_no = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'organization'

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.company_name


class Department(models.Model):
    pub_id = models.CharField(max_length=8, unique=True, default=generate_pub_id, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    dept_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'department'


class Manager(models.Model):
    pub_id = models.CharField(max_length=8, unique=True, default=generate_pub_id, editable=False)
    emp_code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=20)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'manager'


class SupportAgent(models.Model):
    pub_id = models.CharField(max_length=8, unique=True, default=generate_pub_id, editable=False)
    emp_code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=20)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    manager = models.ForeignKey(Manager, on_delete=models.PROTECT, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'support_agent'


class Employee(models.Model):
    pub_id = models.CharField(max_length=8, unique=True, default=generate_pub_id, editable=False)
    emp_code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=20)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'employee'


class DepartmentOnCallSchedule(models.Model):
    pub_id = models.CharField(max_length=8, unique=True, default=generate_pub_id, editable=False)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    start_date = models.DateField()
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'department_on_call_schedule'


class Priority(models.Model):
    pub_id = models.CharField(max_length=8, unique=True, default=generate_pub_id, editable=False)
    priority = models.CharField(max_length=100)
    duration = models.DurationField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'priority'


class CreateTicket(models.Model):
    pub_id = models.CharField(max_length=8, unique=True, default=generate_pub_id, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.ForeignKey(Priority, on_delete=models.PROTECT)
    attachment = models.FileField(upload_to='ticket_attachments', null=True, blank=True)
    status = models.CharField(max_length=100, default='Open')
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    assign_to = models.ForeignKey(SupportAgent, on_delete=models.PROTECT)
    escalated_to = models.ForeignKey(Manager, on_delete=models.PROTECT, null=True)
    escalated_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'create_ticket'


class Comment(models.Model):
    pub_id = models.CharField(max_length=8, unique=True, default=generate_pub_id, editable=False)
    comment = models.TextField()
    ticket = models.ForeignKey(CreateTicket, on_delete=models.PROTECT)
    support_agent = models.ForeignKey(SupportAgent, on_delete=models.PROTECT, null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True, blank=True)
    manager = models.ForeignKey(Manager, on_delete=models.PROTECT, null=True, blank=True)
    order = models.IntegerField()
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comment'
