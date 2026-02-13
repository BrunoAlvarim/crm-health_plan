from django.db import models
from uuid import uuid4

class Customer(models.Model):
    TYPE = [
        ('pf', 'Pessoa Fisica'),
        ('pj', 'Pessoa Juridica'),
    ]
    customer_cod = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    customer_type = models.CharField(max_length=10, choices=TYPE)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    business_group = models.CharField(max_length=100, null=True, blank=True)
    company_segmentation = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    row_id = models.UUIDField(default=uuid4, editable=False, unique=True)
    def __str__(self):
        return f"{self.name}"
    class Meta:
        db_table = "api.customer"
        constraints = [
                    models.UniqueConstraint(fields=['customer_cod'],condition=models.Q(is_active=True),name='unique_active_customer_cod')
                ]
class Plan(models.Model):
    plan_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    row_id = models.UUIDField(default=uuid4, editable=False, unique=True)
    def __str__(self):
        return f"{self.name} ({self.category})"
    class Meta:
        db_table = "api.plan"
        constraints = [
                    models.UniqueConstraint(fields=['plan_id'],condition=models.Q(is_active=True),name='unique_active_plan_id')
                ]        
 
class Lead(models.Model):
    customer  = models.ForeignKey(Customer,on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan,on_delete=models.CASCADE)
    lead_data = models.DateTimeField()
    source = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    row_id = models.UUIDField(default=uuid4, editable=False, unique=True)
    def __str__(self):
        return super().__str__()
    class Meta:
        db_table = "api.lead"

class Opportunities(models.Model):
    customer  = models.ForeignKey(Customer,on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan,on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead,on_delete=models.SET_NULL,null=True,blank=True)    
    open_date = models.DateTimeField()
    close_date = models.DateTimeField()
    status = models.CharField(max_length=100)
    source = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    row_id = models.UUIDField(default=uuid4, editable=False, unique=True)
    def __str__(self):
        return super().__str__()
    class Meta:
        db_table = "api.opportunities"

class Sales(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan,on_delete=models.CASCADE)
    opportunities = models.ForeignKey(Opportunities,on_delete=models.SET_NULL,null=True,blank=True)    
    sale_date = models.DateTimeField()
    start_plan_data = models.DateTimeField()
    end_plan_data = models.DateTimeField()
    monthly_amount = models.DecimalField(max_digits=6,decimal_places=2)
    total_dependents = models.SmallIntegerField()
    observation = models.CharField(max_length=400)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    row_id = models.UUIDField(default=uuid4, editable=False, unique=True)
    def __str__(self):
        return super().__str__()
    class Meta:
        db_table = "api.sales"
