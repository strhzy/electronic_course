from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.apps import apps
from .serializers import DynamicModelSerializer
from django.db.models import Field
from .permissions import ModelActionPermission
from .mixins import MethodRestrictionsMixin

class DynamicModelViewSet(MethodRestrictionsMixin,viewsets.ModelViewSet):
    serializer_class = ModelActionPermission
    permission_classes = [DjangoModelPermissions]
    search_fields = []
    default_http_methods_restrictions = {
        'main.order': {
            'disable_methods': ['put', 'delete']
        },
        'main.orderitem': {
            'disable_methods': ['put', 'delete']
        }
    }
    
    def get_queryset(self):
        return self.model.objects.all()
    
    def get_serializer_class(self):
        return type(
            f'Dynamic{self.model.__name__}Serializer',
            (DynamicModelSerializer,),
            {}
        )
    
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['model'] = self.model
        return serializer_class(*args, **kwargs)
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_param = 'q'
    
    @property
    def search_fields(self):
        if hasattr(self, '_search_fields'):
            return self._search_fields
        searchable_fields = []
        for field in self.model._meta.get_fields():
            if isinstance(field, Field) and field.get_internal_type() in [
                'CharField', 'TextField', 'EmailField', 'SlugField',
                'IntegerField', 'FloatField', 'DecimalField', 'DateField',
                'DateTimeField', 'BooleanField', 'UUIDField'
            ]:
                searchable_fields.append(field.name)
        
        self._search_fields = searchable_fields
        return self._search_fields
    
    @search_fields.setter
    def search_fields(self, value):
        self._search_fields = value

    def get_filter_fields(self):
        filter_fields = []
        for field in self.model._meta.get_fields():
            if isinstance(field, Field):
                filter_fields.append(field.name)
        return filter_fields
    
    def get_filterset_fields(self):
        return self.get_filter_fields()
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        for field_name in self.get_filter_fields():
            if field_name in request.query_params:
                queryset = queryset.filter(**{field_name: request.query_params[field_name]})
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)