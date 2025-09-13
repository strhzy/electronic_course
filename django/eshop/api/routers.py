from django.apps import apps
from rest_framework.routers import DefaultRouter
from .views import DynamicModelViewSet

class AutoRegisterRouter(DefaultRouter):
    def __init__(self, *args, **kwargs):
        self.registered_models = set()
        super().__init__(*args, **kwargs)
    
    def register_models(self, exclude_models=None, include_models=None):
        exclude_models = exclude_models or []
        include_models = include_models or []
        all_models = apps.get_models()
        
        for model in all_models:
            model_name = model._meta.model_name
            app_label = model._meta.app_label
            
            # Проверяем, нужно ли регистрировать модель
            if ((include_models and f'{app_label}.{model_name}' not in include_models) or
                (not include_models and model_name in exclude_models)):
                continue
                
            # Проверяем, не зарегистрирована ли модель уже
            model_key = f'{app_label}.{model_name}'
            if model_key not in self.registered_models:
                self.register_model(model)
                self.registered_models.add(model_key)
    
    def register_model(self, model):
        model_name = model._meta.model_name
        app_label = model._meta.app_label
        basename = f'{app_label}-{model_name}'
        
        viewset = type(
            f'{model.__name__}ViewSet',
            (DynamicModelViewSet,),
            {'model': model}
        )
        self.register(model_name, viewset, basename=basename)