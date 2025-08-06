import json
import requests
from typing import List, Optional

from mju_sugang_alarm.dto.request_lecture import RequestLecture
from mju_sugang_alarm.dto.response_lecture import ResponseLecture, LectureSearchResponse
from mju_sugang_alarm.course_list_crawler.authenticator import Authenticator

from mju_sugang_alarm.exceptions import NotLoggedInError, ConnectionFailedError


class LectureDataFetcher:
    """강의 데이터를 가져오는 클래스 - 데이터 fetching 책임만 담당"""
    
    def __init__(self, authenticator: Authenticator, verbose: bool = False):
        """
        초기화
        
        Args:
            authenticator: 로그인된 Authenticator 인스턴스
            verbose: 상세 로그 출력 여부
        """
        self.authenticator = authenticator
        self.verbose = verbose
        self.base_url = "https://class.mju.ac.kr"
        
    def _log(self, message: str):
        """로그 메시지를 출력합니다."""
        if self.verbose:
            print(message)
    
    def fetch_lectures(self, request: RequestLecture) -> Optional[LectureSearchResponse]:
        """
        강의 검색 API 호출
        
        Args:
            request: 강의 검색 요청 DTO
            
        Returns:
            LectureSearchResponse: 검색 결과, 실패 시 None
        """
        try:
            session = self.authenticator.get_session()
            
            # CSRF 토큰과 헤더 정보 가져오기
            try:
                csrf_header, csrf_token = self.authenticator.get_csrf_token()
            except Exception as e:
                self._log(f"❌ CSRF 토큰 획득 실패: {e}")
                return None
            
            self._log(f"🔍 강의 검색 중: {request.to_dict()}")
            
            # 요청 데이터 구성
            request_data = request.to_dict()
            request_data['_csrf'] = csrf_token
            
            # 헤더 구성
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": f"{self.base_url}/main?lang=ko",
                csrf_header: csrf_token
            }
            
            # AJAX 요청
            response = session.post(
                f"{self.base_url}/ajax/lectureSearch",
                data=request_data,
                timeout=10,
                headers=headers
            )
            
            # 응답 상태 확인
            if response.status_code == 403:
                self._log("⚠️ 403 Forbidden - CSRF 토큰 갱신 시도 중...")
                
                # CSRF 토큰 새로고침 시도
                if self.authenticator.refresh_csrf_token():
                    csrf_header, csrf_token = self.authenticator.get_csrf_token()
                    request_data['_csrf'] = csrf_token
                    headers[csrf_header] = csrf_token
                    
                    self._log("🔄 갱신된 토큰으로 재요청 중...")
                    
                    # 재요청
                    response = session.post(
                        f"{self.base_url}/ajax/lectureSearch",
                        data=request_data,
                        timeout=10,
                        headers=headers
                    )
                    
                    if response.status_code == 403:
                        self._log("❌ 토큰 갱신 후에도 403 Forbidden - 권한 문제일 수 있습니다.")
                        self._log(f"📋 요청 데이터: {request_data}")
                        self._log(f"📋 요청 헤더: {headers}")
                        self._log(f"📋 응답 내용 (처음 500자): {response.text[:500]}")
                        return None
                else:
                    self._log("❌ CSRF 토큰 갱신 실패")
                    return None
            
            response.raise_for_status()
            
            # JSON 응답 파싱
            try:
                lectures_data = response.json()
            except json.JSONDecodeError as json_error:
                self._log(f"❌ JSON 파싱 오류: {json_error}")
                self._log(f"📋 응답 내용: {response.text[:1000]}")
                return None
            
            if not isinstance(lectures_data, list):
                self._log(f"❌ 예상치 못한 응답 형식: {type(lectures_data)}")
                self._log(f"📋 응답 내용: {lectures_data}")
                return None
            
            self._log(f"✅ {len(lectures_data)}개 강의 검색 완료")
            
            # DTO로 변환
            lecture_response = LectureSearchResponse.from_list(lectures_data)
            
            return lecture_response
            
        except NotLoggedInError:
            self._log("❌ 로그인이 필요합니다.")
            return None
        except requests.exceptions.RequestException as e:
            self._log(f"❌ 네트워크 오류: {e}")
            # 응답 내용 로깅 (디버깅용)
            if hasattr(e, 'response') and e.response is not None:
                self._log(f"📋 응답 상태: {e.response.status_code}")
                self._log(f"📋 응답 내용: {e.response.text[:500]}")
            raise ConnectionFailedError(f"강의 검색 중 네트워크 오류: {e}") from e
        except Exception as e:
            self._log(f"❌ 예기치 못한 오류: {e}")
            return None