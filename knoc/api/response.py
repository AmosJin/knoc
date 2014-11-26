from rest_framework.response import Response
from rest_framework.status import *
from api import status as st

class Result(Response):
    def __init__(self, msg='', data={}, status=st.SUCCESS,
                 template_name=None, headers=None,
                 exception=False, content_type=None):

        msg = msg or st.DEFAULT_MSG[status]
        self.wrap_data = {}
        self.wrap_data['status_code'] = status
        self.wrap_data['msg'] = msg
        self.wrap_data['data'] = data
        super(Result, self).__init__(self.wrap_data, HTTP_200_OK,
                                     template_name, headers,
                                     exception, content_type)

SuccessResult = Result

class FailedResult(Result):
    def __init__(self, msg='', data={}, status=st.FAILED):
        super(FailedResult, self).__init__(data=data, msg=msg, status=status)

class BadRequestResult(Result):
    def __init__(self, msg='', data={}, status=HTTP_400_BAD_REQUEST):
        super(BadRequestResult, self).__init__(data=data, msg=msg, status=status)

class ForbiddenResult(Result):
    # we use 401 for forbidden result 
    def __init__(self, msg='', data={}, status=HTTP_401_UNAUTHORIZED):
        super(ForbiddenResult, self).__init__(data=data, msg=msg, status=status)
        
class NotFoundResult(SuccessResult):
    def __init__(self, msg="", data={}, st=HTTP_404_NOT_FOUND):
        super(NotFoundResult, self).__init__(msg,data,st)

class DuplicatedResult(SuccessResult):
    def __init__(self, msg="", data={}, st=HTTP_409_CONFLICT):
        super(DuplicatedResult, self).__init__(msg,data,st)

class NotHereResult(SuccessResult):
    def __init__(self, msg="", data={}, st=HTTP_410_GONE):
        super(NotHereResult, self).__init__(msg,data,st)

class InternalErrorResult(SuccessResult):
    def __init__(self, msg="", data={}, st=HTTP_500_INTERNAL_SERVER_ERROR):
        super(InternalErrorResult, self).__init__(msg,data,st)

class RedirectResult(SuccessResult):
    def __init__(self,msg="",data={},st=HTTP_302_FOUND):
        super(RedirectResult, self).__init__(msg,data,st)
