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

class Plan(ModelViewSet):
    queryset = models.Plan.objects.filter(is_active = True).order_by('id')
    serializer_class = serializers.PlanSerializer
    pagination_class = Pagination