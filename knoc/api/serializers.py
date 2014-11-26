from django.db.models.query import QuerySet
from django.contrib.auth.models import User

class Options(object):
    """
    Meta class options for Serializer
    """
    def __init__(self, model):
        try:
            meta = model.Manifest
        except AttributeError:
            meta = None
            
        self.fields = getattr(meta, 'fields', [])
        self.excludes = getattr(meta, 'excludes', [])
        self.properties = getattr(meta, 'properties', [])
        self.extra = getattr(meta, 'extra', None)
        
class Serializer(object):
    def __init__(self, instance):
        if hasattr(instance, '__iter__'):
            if not instance:
                # instance is an empty list
                self._data = []
                return
            
            self.many = True
            if isinstance(instance, QuerySet):
                self.model = instance.model
            else:
                self.model = instance[0]._meta.concrete_model
        else:
            self.many = False
            self.model = instance._meta.concrete_model

        self._default_fields = None
        self._rel_fields = None
        self._data = None
        self.object = instance
        self.config(Options(self.model))

    @property
    def default_fields(self):
        if self._default_fields is not None:
            return self._default_fields
        self._default_fields = self.model._meta.fields
        return self._default_fields
    
    @property
    def rel_fields(self):
        if self._rel_fields is not None:
            return self._rel_fields
        
        self._rel_fields = dict(((f.name, f.column) for f in self.default_fields if f.rel))
        return self._rel_fields

    def config(self, opts):
        fields = opts.fields or [f.column for f in self.default_fields]
        if opts.excludes:
            """
            add field.column to `excludes` if the field.name  is in excludes
            """
            # copy the list
            excludes = list(opts.excludes)
            for name in opts.excludes:
                if name in self.rel_fields:
                    excludes.append(self.rel_fields[name])
                    
            fields = list(set(fields) - set(excludes))
        if opts.properties:
            fields = list(set(fields) | set(opts.properties))

        self.fields = fields
        self.extra = opts.extra
    
    def to_native(self, obj):
        result = dict(((f, getattr(obj, f)) for f in self.fields))
        if self.extra:
            result.update(self.extra(obj))
            
        return result
    
    @property
    def data(self):
        if self._data is not None:
            return self._data

        obj = self.object
        if self.many:
            self._data = [self.to_native(item) for item in obj]
        else:
            self._data = self.to_native(obj)

        return self._data
            
        
