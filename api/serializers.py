from rest_framework import serializers
import api.models as models

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        exclude = ['created_at', 'updated_at','is_active','row_id']

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Plan
        exclude = ['created_at', 'updated_at','is_active','row_id']
    