from rest_framework.permissions import BasePermission

class ModelActionPermission(BasePermission):
    MODEL_PERMISSIONS = {
        'main.Order': {
            'GET': ['is_authenticated'],
            'POST': ['is_authenticated'],
            'PUT': ['is_staff'],
            'DELETE': [],
        },
        'main.OrderItem': {
            'GET': ['is_authenticated'],  
            'POST': ['is_authenticated'],
            'PUT': ['is_staff'],
            'DELETE': [],
        }
    }

    def has_permission(self, request, view):
        model_name = f"{view.queryset.model._meta.app_label}.{view.queryset.model.__name__}"
        method = request.method.upper()

        if model_name not in self.MODEL_PERMISSIONS:
            return True

        if method not in self.MODEL_PERMISSIONS[model_name]:
            return True
            
        required_perms = self.MODEL_PERMISSIONS[model_name][method]

        for perm in required_perms:
            if perm == 'is_authenticated' and not request.user.is_authenticated:
                return False
            if perm == 'is_staff' and not request.user.is_staff:
                return False
            if perm == 'is_superuser' and not request.user.is_superuser:
                return False
                
        return True