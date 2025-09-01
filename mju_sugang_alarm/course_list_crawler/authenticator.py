"""
로그인 관련 클래스
    1. login 수행
    2. CSRF 토큰 관리
    3. 세션 유효성 검증
    4. 세션 반환
"""


from typing import Optional, Tuple
import requests
from bs4 import BeautifulSoup



from mju_sugang_alarm.exceptions import CSRFTokenNotFoundError, NotLoggedInError, SessionExpiredError, ConnectionFailedError, LoginFailedError


class Authenticator:
    def __init__(self, verbose: bool = False):
        """
        초기화
        
        Args:
            verbose (bool): 상세 로그 출력 여부 (기본값: False)
        """
        self.session = requests.Session()
        self.csrf_token = None
        self.csrf_header = None
        self.is_logged_in = False
        self.verbose = verbose
        self.base_url = "https://class.mju.ac.kr"
        
        # 브라우저처럼 보이게 User-Agent 설정
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        })
        
    def _log(self, message: str):
        """로그 메시지를 출력합니다."""
        if self.verbose:
            print(message)
    
    def _get_csrf_token(self) -> None:
        """
        로그인 페이지에서 CSRF 토큰을 BeautifulSoup으로 추출
        성공 시 self.csrf_token에 저장, 실패 시 CSRFTokenNotFoundError 발생
        """
        self._log("🔄 로그인 페이지 접속 중...")

        try:
            response = self.session.get(f"{self.base_url}/", timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self._log(f"❌ 접속 실패: {e}")
            raise CSRFTokenNotFoundError(f"서버 접속 실패: {e}") from e

        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_input = soup.find('input', {'name': '_csrf'})

        if not csrf_input or not csrf_input.get('value'):
            self._log("❌ CSRF 토큰을 찾을 수 없습니다.")
            raise CSRFTokenNotFoundError("HTML에서 _csrf 토큰을 찾을 수 없습니다.")

        self.csrf_token = csrf_input['value']
        self._log(f"✅ CSRF 토큰 획득: {self.csrf_token}")
    
    def get_csrf_token(self) -> Tuple[str, str]:
        """
        캐시된 CSRF 토큰과 헤더 정보를 반환 (네트워크 요청 없음)
        
        Returns:
            tuple[str, str]: (헤더명, 토큰값) 튜플
            
        Raises:
            CSRFTokenNotFoundError: CSRF 정보가 캐시되지 않은 경우
            NotLoggedInError: 로그인이 되어있지 않은 경우
        """
        if not self.is_logged_in:
            self._log("❌ 로그인이 되어있지 않습니다.")
            raise NotLoggedInError()
        
        if not self.csrf_token or not self.csrf_header:
            self._log("❌ CSRF 토큰이 캐시되지 않았습니다. 로그인을 다시 시도하세요.")
            raise CSRFTokenNotFoundError("CSRF 토큰이 캐시되지 않았습니다.")
        
        self._log(f"✅ 캐시된 CSRF 정보 반환 - 헤더: {self.csrf_header}")
        self._log(f"✅ 캐시된 CSRF 정보 반환 - 토큰: {self.csrf_token}")
        
        return self.csrf_header, self.csrf_token
    
    def login(self, username: str, password: str) -> bool:
        """
        로그인 수행
    
        Args:
            username (str): 학번
            password (str): 비밀번호
    
        Returns:
            bool: 로그인 성공 여부
        """
        try:
            # 1. CSRF 토큰 획득 (실패 시 예외 발생)
            self._get_csrf_token()
    
            # 2. 로그인 데이터 구성
            login_data = {
                "username": username.strip(),
                "password": password,
                "lang": "ko",
                "_csrf": self.csrf_token,
            }
    
            # 3. 로그인 요청
            self._log("🔐 로그인 요청 중...")
            login_response = self.session.post(
                f"{self.base_url}/loginproc",
                data=login_data,
                allow_redirects=True,
                timeout=10,
            )
    
            # 4. 응답 상태 확인
            if login_response.status_code != 200:
                self._log(f"❌ HTTP 오류: {login_response.status_code}")
                return False
    
            # 5. 로그인 성공 여부 판단
            final_url = login_response.url
            if "main" in final_url:
                self._log("🎉 로그인 성공!")
                self._log(f"🏠 메인 페이지 접속: {final_url}")
                self.is_logged_in = True
                
                # 6. 로그인 성공 시 즉시 메인 페이지의 CSRF 토큰 캐싱
                self._cache_main_csrf_token()
                return True
    
            # 로그인 실패 여부 확인
            content = login_response.text
            if "로그인" in content or "Sign in" in content or "login" in content.lower():
                self._log("❌ 로그인 실패: 학번 또는 비밀번호를 확인하세요.")
            else:
                self._log("⚠️ 로그인 실패: 보안 차단 또는 일시적 오류일 수 있습니다.")
    
            self._log(f"📍 현재 URL: {final_url}")
            return False
    
        except CSRFTokenNotFoundError as e:
            self._log(f"🚫 인증 토큰 오류: {e}")
            return False
        except requests.exceptions.RequestException as e:
            self._log(f"🌐 네트워크 오류: {e}")
            return False
        except Exception as e:
            self._log(f"❗ 예기치 못한 오류: {e}")
            return False
    
    def _cache_main_csrf_token(self) -> None:
        """
        메인 페이지에서 CSRF 토큰과 헤더 정보를 캐싱
        로그인 성공 직후 호출하여 이후 요청에서 재사용
        """
        self._log("🔄 메인 페이지 CSRF 토큰 캐싱 중...")
        
        try:
            response = self.session.get(f"{self.base_url}/main?lang=ko", timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self._log(f"❌ 메인 페이지 접속 실패: {e}")
            return
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # CSRF 토큰 추출
        csrf_meta = soup.find('meta', {'name': '_csrf'})
        csrf_header_meta = soup.find('meta', {'name': '_csrf_header'})
        
        if csrf_meta and csrf_meta.get('content') and csrf_header_meta and csrf_header_meta.get('content'):
            self.csrf_token = csrf_meta['content']
            self.csrf_header = csrf_header_meta['content']
            self._log(f"✅ CSRF 토큰 캐싱 완료 - 헤더: {self.csrf_header}")
            self._log(f"✅ CSRF 토큰 캐싱 완료 - 토큰: {self.csrf_token}")
        else:
            self._log("⚠️ CSRF 토큰 캐싱 실패 - 메타태그를 찾을 수 없습니다.")
    
    def refresh_csrf_token(self) -> bool:
        """
        CSRF 토큰을 새로고침 (세션 만료 시 호출)
        
        Returns:
            bool: 토큰 갱신 성공 여부
        """
        self._log("🔄 CSRF 토큰 새로고침 중...")
        try:
            self._cache_main_csrf_token()
            return self.csrf_token is not None and self.csrf_header is not None
        except Exception as e:
            self._log(f"❌ CSRF 토큰 새로고침 실패: {e}")
            return False
    
    def verify_session(self) -> bool:
        """세션 유효성 검증 (메인 페이지 접근 테스트)"""
        if not self.is_logged_in:
            self._log("❌ 로그인이 되어있지 않습니다.")
            self.is_logged_in = False
            raise NotLoggedInError()

        self._log("🔍 세션 유효성 검증 중...")
        try:
            main_response = self.session.get(f"{self.base_url}/main?lang=ko", timeout=10)
            main_response.raise_for_status()  # HTTP 에러 상태 코드 시 예외 발생

            if "로그아웃" in main_response.text:
                self._log("✅ 세션이 유효합니다.")
                return True
            else:
                self._log("❌ 세션이 만료되었거나 유효하지 않습니다.")
                self.is_logged_in = False
                raise SessionExpiredError()

        except requests.exceptions.RequestException as e:
            self._log(f"❌ 세션 검증 실패: {e}")
            self.is_logged_in = False
            raise ConnectionFailedError(f"세션 검증 중 네트워크 오류: {e}") from e


    def get_session(self) -> requests.Session:
        """로그인된 세션 반환 (예외 발생 방식)"""
        if self.is_logged_in and self.session is not None:
            return self.session
        else:
            self._log("❌ 로그인이 되어있지 않습니다.")
            raise NotLoggedInError()
    
    
    
        
            
    
    
