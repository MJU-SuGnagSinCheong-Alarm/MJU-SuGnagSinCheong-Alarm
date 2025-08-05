# exceptions.py


## 명지대학교 수강신청 시스템 관련 예외 정의
class MJUClassException(Exception):
    """명지대학교 수강신청 시스템 관련 예외의 기본 클래스"""
    pass


class ConnectionFailedError(MJUClassException):
    """로그인 페이지 접속 실패 시 발생"""
    def __init__(self, message="서버 연결에 실패했습니다."):
        self.message = message
        super().__init__(self.message)

class LoginFailedError(MJUClassException):
    """로그인 실패 시 발생"""
    def __init__(self, message="로그인에 실패했습니다."):
        self.message = message
        super().__init__(self.message)

class CSRFTokenNotFoundError(MJUClassException):
    """CSRF 토큰을 페이지에서 찾지 못했을 때 발생"""
    def __init__(self, message="CSRF 토큰을 페이지에서 찾을 수 없습니다."):
        self.message = message
        super().__init__(self.message)
        
class SessionExpiredError(MJUClassException):
    """세션 유효성 검사 실패 (세션이 만료됨)"""
    def __init__(self, message="세션이 만료되었거나 유효하지 않습니다."):
        self.message = message
        super().__init__(self.message)


class NotLoggedInError(MJUClassException):
    """로그인되지 않은 상태에서 세션 접근 시도할 때 발생"""
    def __init__(self, message="로그인이 필요합니다."):
        self.message = message
        super().__init__(self.message)


