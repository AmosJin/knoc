from django.http import Http404

class Result404(Http404):
    def __init__(self, msg):
        self.msg = msg

class DataFormatError(Exception):
    def __init__(self, msg):
        self.msg = msg
        
