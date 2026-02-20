from rest_framework import viewsets
import api.models as models 
import api.serializers as serializers
from rest_framework.pagination import PageNumberPagination

class Pagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100

class ModelViewSet(viewsets.ModelViewSet):
    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)
    def perform_destroy(self, instance):
        try:
            instance.is_active = False
            instance.save()
            return True
        except:
            return False
class Customer(ModelViewSet):
    queryset = models.Customer.objects.filter(is_active = True).order_by('id')
    serializer_class = serializers.CustomerSerializer
    pagination_class = Pagination
    filterset_fields = {
        "updated_at": ["gte", "lte"]
    }  
class Plan(ModelViewSet):
    queryset = models.Plan.objects.filter(is_active = True).order_by('id')
    serializer_class = serializers.PlanSerializer
    pagination_class = Pagination
    filterset_fields = {
        "updated_at": ["gte", "lte"]
    }  
class Lead(ModelViewSet):
    queryset = models.Lead.objects.filter(is_active = True).order_by('id')
    serializer_class = serializers.LeadSerializer
    pagination_class = Pagination
    filterset_fields = {
        "updated_at": ["gte", "lte"]
    }    
class Opportunities(ModelViewSet):
    queryset = models.Opportunities.objects.filter(is_active = True).order_by('id')
    serializer_class = serializers.OpportunitiesSerializer
    pagination_class = Pagination
    filterset_fields = {
        "updated_at": ["gte", "lte"]
    }  
class Sales(ModelViewSet):
    queryset = models.Sales.objects.filter(is_active = True).order_by('id')
    serializer_class = serializers.SalesSerializer
    pagination_class = Pagination
    filterset_fields = {
        "updated_at": ["gte", "lte"]
    }      