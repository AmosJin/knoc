import re
import inspect
from rest_framework import status

SUCCESS = 0
FAILED = 1
DEFAULT_MSG = {
    SUCCESS:'SUCCESS',
    FAILED:'FAILED'
}

for st,code in inspect.getmembers(status, predicate=lambda x:isinstance(x,int)):
    _,msg = re.search(r'HTTP_(\d+)_([\w_]+)', st).groups()
    DEFAULT_MSG.update({code:msg})
