from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer

class MethodRestrictionsMixin:
    default_http_methods_restrictions = {
        '*': {'disable_methods': []}
    }
    
    def get_model_name(self):
        return f"{self.model._meta.app_label}.{self.model.__name__.lower()}"
    
    def get_method_restrictions(self):
        model_name = self.get_model_name()
        restrictions = self.default_http_methods_restrictions.get('*', {}).copy()
        restrictions.update(self.default_http_methods_restrictions.get(model_name, {}))
        return restrictions
    
    def is_method_allowed(self, method):
        restrictions = self.get_method_restrictions()
        return method.lower() not in restrictions.get('disable_methods', [])
    
    def _get_allowed_methods(self):
        restrictions = self.get_method_restrictions()
        disabled_methods = restrictions.get('disable_methods', [])
        return [m.upper() for m in ['get', 'post', 'put', 'patch', 'delete'] 
                if m not in disabled_methods]
    
    def _method_not_allowed_response(self, request, method):
        response = Response(
            {
                "detail": f"Method {method.upper()} not allowed for this model",
                "model": self.get_model_name(),
                "allowed_methods": self._get_allowed_methods()
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {"view": self}
        return response
    
    def dispatch(self, request, *args, **kwargs):
        method = request.method.lower()
        if not self.is_method_allowed(method):
            return self._method_not_allowed_response(request, method)
        return super().dispatch(request, *args, **kwargs)