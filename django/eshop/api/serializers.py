from rest_framework import serializers
from django.apps import apps

class DynamicModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        model = kwargs.pop('model', None)
        fields = kwargs.pop('fields', '__all__')
        exclude = kwargs.pop('exclude', None)
        depth = kwargs.pop('depth', 0)
        
        super().__init__(*args, **kwargs)
        
        if model:
            self.Meta.model = model
            self.Meta.fields = fields
            if exclude:
                self.Meta.exclude = exclude
            self.Meta.depth = depth

    class Meta:
        model = None
        fields = '__all__'
        depth = 0