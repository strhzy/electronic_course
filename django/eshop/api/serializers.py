from rest_framework import serializers

class DynamicModelSerializer(serializers.ModelSerializer):
    class Meta:
        pass

    def __init__(self, *args, **kwargs):
        model = kwargs.pop('model', None)
        fields = kwargs.pop('fields', '__all__')
        exclude = kwargs.pop('exclude', None)
        depth = kwargs.pop('depth', 0)
        super().__init__(*args, **kwargs)

        if model:
            meta_attrs = {'model': model, 'fields': fields, 'depth': depth}
            if exclude:
                meta_attrs['exclude'] = exclude
            self.Meta = type('Meta', (), meta_attrs)
            self.__class__.Meta = self.Meta