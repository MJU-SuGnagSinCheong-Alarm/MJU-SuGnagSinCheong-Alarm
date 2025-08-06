import json
import requests
from typing import List, Optional

from mju_sugang_alarm.dto.request_lecture import RequestLecture
from mju_sugang_alarm.dto.response_lecture import ResponseLecture, LectureSearchResponse
from mju_sugang_alarm.repository.lecture_repository import CourseRepository
from mju_sugang_alarm.course_list_crawler.authenticator import Authenticator

from mju_sugang_alarm.exceptions import NotLoggedInError, ConnectionFailedError


class LectureDataFetcher:
    """강의 데이터를 가져오는 클래스"""
    
    def __init__(self, authenticator: Authenticator, repository: CourseRepository, verbose: bool = False):
        """
        초기화
        
        Args:
            authenticator: 로그인된 Authenticator 인스턴스
            repository: 강의 데이터를 저장할 레포지토리
            verbose: 상세 로그 출력 여부
        """
        self.authenticator = authenticator
        self.repository = repository
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
            # 세션 유효성 검증
            self.authenticator.verify_session()
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
                self._log("❌ 403 Forbidden - CSRF 토큰 또는 권한 문제일 수 있습니다.")
                self._log(f"📋 요청 데이터: {request_data}")
                self._log(f"📋 요청 헤더: {headers}")
                self._log(f"📋 응답 내용 (처음 500자): {response.text[:500]}")
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
    
    def fetch_and_save_lectures(self, request: RequestLecture) -> bool:
        """
        강의 검색 후 레포지토리에 저장
        
        Args:
            request: 강의 검색 요청 DTO
            
        Returns:
            bool: 성공 여부
        """
        result = self.fetch_lectures(request)
        
        if result is not None:
            self.repository.save_lecture_response(result)
            self._log(f"💾 {len(result.lectures)}개 강의 데이터 저장 완료")
            return True
        else:
            self._log("❌ 강의 데이터 저장 실패")
            return False
    
    def fetch_all_lecture_categories(self, lecture_search_data: List[dict]) -> int:
        """
        lecture_search.json의 모든 카테고리에 대해 강의 검색
        
        Args:
            lecture_search_data: lecture_search.json 데이터
            
        Returns:
            int: 성공적으로 처리된 카테고리 수
        """
        success_count = 0
        total_lectures = 0
        
        for i, category_data in enumerate(lecture_search_data):
            # name 필드 제외하고 RequestLecture 객체 생성
            if "name" in category_data:
                category_data_copy = category_data.copy()
                category_name = category_data_copy.pop("name")
                request = RequestLecture.from_dict(category_data_copy)
                
                self._log(f"📚 [{i+1}/{len(lecture_search_data)}] '{category_name}' 카테고리 검색 중...")
                
                if self.fetch_and_save_lectures(request):
                    success_count += 1
                    current_count = self.repository.count()
                    new_lectures = current_count - total_lectures
                    total_lectures = current_count
                    self._log(f"✅ '{category_name}': {new_lectures}개 강의 추가 (누적: {total_lectures}개)")
                else:
                    self._log(f"❌ '{category_name}' 검색 실패")
                
                # 요청 간 잠시 대기 (서버 부하 방지)
                # import time
                # time.sleep(0.01)
        
        self._log(f"🎉 전체 결과: {success_count}/{len(lecture_search_data)} 카테고리 성공, 총 {total_lectures}개 강의 수집")
        return success_count
    
    def load_and_fetch_from_json(self, json_file_path: str) -> int:
        """
        JSON 파일에서 검색 조건을 로드하여 강의 검색
        
        Args:
            json_file_path: lecture_search.json 파일 경로
            
        Returns:
            int: 성공적으로 처리된 카테고리 수
        """
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                lecture_search_data = json.load(f)
            
            # 빈 객체나 불완전한 객체 필터링
            valid_data = []
            for item in lecture_search_data:
                if isinstance(item, dict) and "name" in item and len(item) > 1:
                    # 필수 필드들이 모두 있는지 확인
                    required_fields = ["campusDiv", "deptCd", "displayDiv", "searchType"]
                    if all(field in item for field in required_fields):
                        valid_data.append(item)
            
            self._log(f"📁 JSON 파일에서 {len(valid_data)}개 유효한 카테고리 로드")
            
            return self.fetch_all_lecture_categories(valid_data)
            
        except FileNotFoundError:
            self._log(f"❌ 파일을 찾을 수 없습니다: {json_file_path}")
            return 0
        except json.JSONDecodeError as e:
            self._log(f"❌ JSON 파싱 오류: {e}")
            return 0
        except Exception as e:
            self._log(f"❌ 파일 로드 오류: {e}")
            return 0