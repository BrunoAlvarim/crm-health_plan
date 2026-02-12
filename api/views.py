from rest_framework import viewsets
import api.models as models 
import api.serializers as serializers
from rest_framework.pagination import PageNumberPagination

class Pagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100

class BulkModelViewSet(viewsets.ModelViewSet):
    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)

class Customer(BulkModelViewSet):
    queryset = models.Customer.objects.all().order_by('id')
    serializer_class = serializers.CustomerSerializer
    pagination_class = Pagination

class Plan(BulkModelViewSet):
    queryset = models.Plan.objects.all().order_by('id')
    serializer_class = serializers.PlanSerializer
    pagination_class = Pagination    