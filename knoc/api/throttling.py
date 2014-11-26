from rest_framework.throttling import SimpleRateThrottle

class UserRateThrottle(SimpleRateThrottle):
    scope = 'user'

    def get_cache_key(self, request, view):
        if not request.user.is_authenticated():
            return None
        
        return self.cache_format % {
            'scope': self.scope,
            'ident': request.user.id
        }

class ClientRateThrottle(SimpleRateThrottle):
    scope = 'client'

    def get_cache_key(self, request, view):
        if not (request.auth and request.user.is_authenticated()):
            return None
        
        ident = '%s' % (request.user.id)
        
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }
